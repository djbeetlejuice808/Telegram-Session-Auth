import os
from dotenv import load_dotenv

# Nạp biến môi trường
load_dotenv()

# Thông tin API Telegram
API_ID = os.getenv('TELEGRAM_API_ID')
API_HASH = os.getenv('TELEGRAM_API_HASH')
PHONE_NUMBER = os.getenv('TELEGRAM_PHONE')