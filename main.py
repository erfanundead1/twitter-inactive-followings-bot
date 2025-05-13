import os
import subprocess
from telegram import Bot

# تنظیمات
USERNAME = os.getenv("TWITTER_USERNAME")
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# اجرای Twint برای گرفتن فالوئینگ‌ها
def get_following_list(username):
    subprocess.run(["twint", "-u", username, "--following", "-o", "following.txt", "--csv"])
    with open("following.txt", "r", encoding="utf-8") as f:
        return list(set([line.split(",")[1] for line in f.readlines()[1:]]))

# بررسی فعالیت کاربران
def check_inactive_users(users):
    inactive = []
    for user in users:
        result = subprocess.run(["twint", "-u", user, "--since", "2025-03-13", "--limit", "1"], capture_output=True)
        if not result.stdout:
            inactive.append(f"https://twitter.com/{user}")
    return inactive

# ارسال به تلگرام
def send_to_telegram(links):
    if not links:
        return
    msg = "لیست افرادی که دو ماه هیچ فعالیتی نداشتن:\n\n" + "\n".join(links)
    bot = Bot(token=BOT_TOKEN)
    bot.send_message(chat_id=CHAT_ID, text=msg)

def main():
    following = get_following_list(USERNAME)
    inactive_users = check_inactive_users(following)
    send_to_telegram(inactive_users)

if __name__ == "__main__":
    main()
