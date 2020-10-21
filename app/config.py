import os
from dotenv import load_dotenv
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

# BOT information
TELEGRAM_API_TOKEN = os.environ.get('TELEGRAM_API_TOKEN')
WEBHOOK_URL = os.environ.get('WEBHOOK_URL')
REPLACE_SEPARATOR = os.environ.get('REPLACE_SEPARATOR')
FLASK_DEBUG = bool(int(os.environ.get('FLASK_DEBUG')))

# remote server information
BASE_URL = os.environ.get('BASE_URL')
AUTH_TOKEN = os.environ.get('AUTH_TOKEN')
