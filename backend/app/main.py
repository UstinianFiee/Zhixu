from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import create_db_and_tables
from app.auth import router as auth_router
from app.routers.daily import router as daily_router
from app.routers.words import router as words_router
from app.routers.leaderboard import router as leaderboard_router
from app.routers.points import router as points_router
from app.routers.admin import router as admin_router

app = FastAPI(title="知序 Zhixu API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000", "http://localhost:1234"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/api/auth", tags=["认证"])
app.include_router(daily_router, prefix="/api", tags=["每日内容"])
app.include_router(words_router, prefix="/api", tags=["单词学习"])
app.include_router(leaderboard_router, prefix="/api", tags=["排行榜"])
app.include_router(points_router, prefix="/api", tags=["积分"])
app.include_router(admin_router, prefix="/api", tags=["后台管理"])


@app.on_event("startup")
def on_startup():
    import time
    for attempt in range(10):
        try:
            create_db_and_tables()
            print("数据库表初始化成功")
            return
        except Exception as e:
            print(f"数据库初始化失败 ({attempt+1}/10): {e}")
            time.sleep(3)
    print("警告: 数据库初始化跳过，部分功能可能不可用")


@app.get("/")
def root():
    return {"message": "知序 API 运行中", "docs": "/docs"}
