import os
import yt_dlp
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

# BotFather से मिला हुआ token
TOKEN = "8483257931:AAHc05I4EvOW3FxYuULECZfG2qQw7dKyxj4"

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# Start command
@dp.message_handler(commands=['start'])
async def start_cmd(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("📥 Download Reels", "ℹ️ Help")
    await message.answer("Welcome to CROFON Reels Downloader Bot 🚀", reply_markup=keyboard)

# Help button
@dp.message_handler(lambda message: message.text == "ℹ️ Help")
async def help_cmd(message: types.Message):
    help_text = """🤖 CROFON Reels Downloader Bot

Steps:
1. Press /start
2. Click 📥 Download Reels button
3. Paste Instagram Reel or YouTube Short link
4. Get your video!

Supported Platforms:
✅ Instagram Reels/Posts/Videos
✅ YouTube Shorts/Videos

About:
Fast downloader powered by yt-dlp

Powered by: @CROFON
Support: @CROFONCHAT"""
    await message.answer(help_text)

# Download button
@dp.message_handler(lambda message: message.text == "📥 Download Reels")
async def download_cmd(message: types.Message):
    await message.answer("Send me the Instagram Reel or YouTube Short link 🔗")

# Handle links
@dp.message_handler(lambda message: "instagram.com" in message.text or "youtu" in message.text)
async def handle_link(message: types.Message):
    url = message.text
    await message.answer("Downloading your video... ⏳")

    try:
        # yt-dlp options
        ydl_opts = {
            'format': 'mp4',
            'outtmpl': 'downloaded_video.%(ext)s'
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        # Send video back
        await message.answer_video(open("downloaded_video.mp4", "rb"))
        os.remove("downloaded_video.mp4")

    except Exception as e:
        await message.answer(f"❌ Error: {e}")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
