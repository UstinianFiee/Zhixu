/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{vue,ts}'],
  theme: {
    extend: {
      colors: {
        'zhixu-blue': '#2C3E50',
        'zhixu-cream': '#F5F0E6',
        'zhixu-gold': '#D4AF37',
        'zhixu-dark': '#1a252f',
        'zhixu-light': '#faf8f3',
      },
      fontFamily: {
        serif: ['"Noto Serif SC"', 'Georgia', 'serif'],
        sans: ['"Inter"', 'system-ui', 'sans-serif'],
      }
    }
  },
  plugins: [],
}
