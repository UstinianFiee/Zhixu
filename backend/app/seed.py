import json
import os
from datetime import date
from sqlmodel import Session, select
from app.database import engine, create_db_and_tables
from app.models import WordList, Word, DailyContent, User, PointTransaction
from app.auth import hash_password


def seed():
    create_db_and_tables()

    with Session(engine) as db:
        # 1. 创建管理员
        admin = db.exec(select(User).where(User.username == "admin")).first()
        if not admin:
            admin = User(
                username="admin",
                email="admin@zhixu.com",
                password_hash=hash_password("admin123"),
                is_admin=True,
                total_points=0,
            )
            db.add(admin)

        # 2. 创建示范用户
        demo = db.exec(select(User).where(User.username == "demo")).first()
        if not demo:
            demo = User(
                username="demo",
                email="demo@zhixu.com",
                password_hash=hash_password("demo123"),
                total_points=500,
                current_level=3,
            )
            db.add(demo)
            db.flush()
            pt = PointTransaction(user_id=demo.id, points_change=500, reason="demo_init")
            db.add(pt)

        db.commit()

        # 3. 导入每日内容
        data_dir = os.path.join(os.path.dirname(__file__), "..", "data")
        daily_file = os.path.join(data_dir, "daily_content.json")
        if os.path.exists(daily_file):
            with open(daily_file, "r", encoding="utf-8") as f:
                contents = json.load(f)
            for item in contents:
                existing = db.exec(
                    select(DailyContent).where(
                        DailyContent.date == date.fromisoformat(item["date"]),
                        DailyContent.type == item["type"],
                    )
                ).first()
                if not existing:
                    dc = DailyContent(
                        date=date.fromisoformat(item["date"]),
                        type=item["type"],
                        title=item["title"],
                        content=item["content"],
                        author=item.get("author"),
                    )
                    db.add(dc)
            print(f"导入每日内容: {len(contents)} 条")

        # 4. 导入词库
        wordlists_data = [
            ("CET-4", "大学英语四级核心词汇", "cet4_full.json"),
            ("CET-6", "大学英语六级核心词汇", "cet6_full.json"),
        ]
        for name, desc, filename in wordlists_data:
            filepath = os.path.join(data_dir, filename)
            if not os.path.exists(filepath):
                print(f"词库文件不存在: {filename}")
                continue

            with open(filepath, "r", encoding="utf-8") as f:
                words_data = json.load(f)

            wl = db.exec(select(WordList).where(WordList.name == name)).first()
            if wl and wl.word_count < len(words_data):
                # Delete old words and reimport
                old_words = db.exec(select(Word).where(Word.wordlist_id == wl.id)).all()
                for w in old_words:
                    db.delete(w)
                db.flush()
                wl = None

            if not wl:
                wl = WordList(name=name, description=desc, is_preset=True)
                db.add(wl)
                db.flush()

            existing_count = db.exec(
                select(Word).where(Word.wordlist_id == wl.id)
            ).first()
            if not existing_count:
                for item in words_data:
                    w = Word(
                        wordlist_id=wl.id,
                        word=item["word"],
                        translation=item["translation"],
                        phonetic=item.get("phonetic"),
                        example_sentence=item.get("example_sentence"),
                    )
                    db.add(w)
                wl.word_count = len(words_data)
                db.add(wl)
                print(f"导入词库 [{name}]: {len(words_data)} 个单词")
            else:
                print(f"词库 [{name}] 已有 {wl.word_count} 个单词，跳过")

        db.commit()
        print("\n种子数据导入完成!")
        print(f"管理员账号: admin / admin123")
        print(f"示范账号: demo / demo123")


if __name__ == "__main__":
    seed()
