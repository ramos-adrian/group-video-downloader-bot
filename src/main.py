import glob
import logging
import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

from utils import is_video_url, get_file_size, get_video_info, get_duration, download

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

load_dotenv()

BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
MAX_FILE_SIZE = 50000000
MAX_DURATION = 60 * 5


async def handle_url_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    first_entity = update.message.entities[0]
    url = update.message.text[first_entity.offset:first_entity.offset + first_entity.length]

    if not is_video_url(url):
        return

    try:
        sanitized_video_info = get_video_info(url)
    except Exception as e:
        await update.message.reply_text('The video could not be downloaded', quote=True)
        return

    try:
        file_size = get_file_size(sanitized_video_info)
    except Exception as e:
        pass
    else:
        if file_size > MAX_FILE_SIZE:
            await update.message.reply_text('File size too large', quote=True)
            return

    try:
        duration = get_duration(sanitized_video_info)
    except Exception as e:
        await update.message.reply_text('The video could not be downloaded', quote=True)
        return
    else:
        if duration > MAX_DURATION:
            await update.message.reply_text('Video too long', quote=True)
            return

    files = glob.glob('video/*.mp4')
    for file in files:
        os.remove(file)

    file_name = download(url)
    await update.message.reply_video(video=open(f'video/{file_name}.mp4', 'rb'), quote=True, disable_notification=True)


def setHandlers(application):
    detect_url_handler = MessageHandler(filters=filters.Entity('url') & filters.ChatType.GROUPS,
                                        callback=handle_url_message)
    application.add_handler(detect_url_handler)


if __name__ == '__main__':
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    setHandlers(application)

    application.run_polling()
