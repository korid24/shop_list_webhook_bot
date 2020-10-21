from flask import Flask, request
import telegram
from config import TELEGRAM_API_TOKEN, FLASK_DEBUG
from bot import ShopListBot
from flask_sslify import SSLify

app = Flask(__name__)
sslify = SSLify(app)

bot = telegram.Bot(token=TELEGRAM_API_TOKEN)


@app.route('/{}/'.format(TELEGRAM_API_TOKEN), methods=['POST', 'GET'])
def index():
    """
    На данный url вешается вебхук, после чего на него поступают запросы от
    телеграма
    """
    if request.method == 'POST':
        r = request.get_json()
        update = telegram.Update.de_json(data=r, bot=bot)
        update_handler = ShopListBot(update)
        update_handler.answer()

        return 'ok'
    return '<h1>ITS WORKING!</h1>'


if __name__ == '__main__':
    app.run(debug=FLASK_DEBUG)
