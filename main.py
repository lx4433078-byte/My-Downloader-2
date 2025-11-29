import os
import asyncio
import logging
import yt_dlp
from aiogram import Bot, Dispatcher, types, F

# Enable logging for Render/Replit logs
logging.basicConfig(level=logging.INFO)

TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    print("ERROR: BOT_TOKEN not found! Check environment variables.")
    exit(1)

bot = Bot(token=TOKEN)
dp = Dispatcher()

# OPTIONAL: Make private (uncomment and add your ID from @userinfobot)
# ALLOWED = 123456789  # Your Telegram ID
# @dp.message(lambda message: message.from_user.id != ALLOWED)
# async def private_block(message: types.Message):
#     await message.reply("This bot is private.")

@dp.message(F.text)
async def any_msg(message: types.Message):
    # Uncomment for private check
    # if message.from_user.id != ALLOWED:
    #     return await message.reply("Private bot.")

    url = message.text.strip()
    if ".m3u8" not in url.lower():
        return await message.reply("Send me a .m3u8 link (Classplus, PW, etc.)")

    msg = await message.reply("Downloading… (3–15 min)")

    ydl_opts = {
        'format': 'best',
        'outtmpl': '%(id)s.%(ext)s',
        'concurrent_fragment_downloads': 15,
        'retries': 30,
        'http_headers': {'Referer': 'https://www.classplusapp.com/'},
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            file = ydl.prepare_filename(info)
            if not file.endswith('.mp4'):
                file = file.rsplit('.', 1)[0] + '.mp4'

        await msg.edit_text("Uploading video…")
        await message.answer_video(types.InputFile(file))
        await msg.delete()
    except Exception as e:
        await msg.edit_text(f"Failed: {str(e)[:300]}")
        print(f"Error: {e}")  # Shows in logs
    finally:
        for f in os.listdir("."):
            if f.endswith(('.mp4', '.mkv', '.webm', '.part', '.ts')):
                try:
                    os.remove(f)
                except:
                    pass

async def main():
    print("Bot is starting…")  # Shows in logs
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
