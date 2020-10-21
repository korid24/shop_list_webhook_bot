import sqlite3
import requests
from config import TELEGRAM_API_TOKEN, WEBHOOK_URL


def set_webhook():
    """
    Вешает вебхук на адрес https://www.example.com/<telegram_api_token>/
    """
    url = ('https://api.telegram.org/bot{}/setWebhook?url={}/{}/'
           .format(TELEGRAM_API_TOKEN, WEBHOOK_URL, TELEGRAM_API_TOKEN))
    requests.get(url=url)

    check_url = ('https://api.telegram.org/bot{}/getWebhookInfo'
                 .format(TELEGRAM_API_TOKEN))
    response = requests.get(url=check_url)
    if response.json().get('ok'):
        return 'webhook установлен на {}/{}/'.format(
            WEBHOOK_URL, TELEGRAM_API_TOKEN)
    raise ConnectionError(
        'не удалось установить webhook на {}/{}/'.format(
            WEBHOOK_URL, TELEGRAM_API_TOKEN))


def create_database():
    """
    Создаёт базу данных
    """
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users
                   (telegram_id int PRIMARY KEY, position int NOT NULL)''')


if __name__ == '__main__':
    print(set_webhook())
    create_database()
