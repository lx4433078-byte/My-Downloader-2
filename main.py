import os, yt_dlp
from aiogram import Bot, Dispatcher, types, executor

TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# ←←← REMOVE THE # FROM NEXT 2 LINES IF YOU WANT PRIVATE BOT ONLY
# ALLOWED = 123456789  # ← put your Telegram ID here (get from @userinfobot)
# if message.from_user.id != ALLOWED: return await message.reply("Private bot")

@dp.message_handler()
async def any_msg(message: types.Message):
    url = message.text.strip()
    if ".m3u8" not in url.lower():
        return await message.reply("Send me a .m3u8 link")

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
                file = file.rsplit('.',1)[0] + '.mp4'
        
        await msg.edit_text("Uploading video…")
        await message.answer_video(types.InputFile(file))
        await msg.delete()
    except Exception as e:
        await msg.edit_text(f"Failed: {str(e)[:300]}")
    finally:
        for f in os.listdir("."):
            if f.endswith(('.mp4','.mkv','.webm','.part','.ts')):
                try: os.remove(f)
                except: pass

executor.start_polling(dp, skip_updates=True)
