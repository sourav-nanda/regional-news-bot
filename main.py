
from src.telegram_client import Telegram
from src.async_get_paper import NewspaperDownloader
from dotenv import load_dotenv
import os

load_dotenv()

location = 'SAMBALPUR'

bot_token = os.getenv('BOT_TOKEN')
chat_id = int(os.getenv('CHAT_ID'))

telegram_bot = Telegram(bot_token)
downloader = NewspaperDownloader()


def send_newspaper(chat_id, telegram_bot, downloader):
    message = 'Good morning ☀️🌇'
    newspaper = downloader.download_newspaper(location)

    telegram_bot.send_message_and_document(chat_id, message, newspaper)



