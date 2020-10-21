import re
from config import TELEGRAM_API_TOKEN, REPLACE_SEPARATOR
from bot_engine.message_handlers import (command_handler, move_handler,
                                         replace_handler, remove_handler,
                                         add_handler)
import telegram


class ShopListBot:
    def __init__(self, update):
        self.update = update
        self._chat_id = self.update.effective_message.chat_id
        self._text = self.update.message.text
        self._user = self.update.effective_user

    bot = telegram.Bot(token=TELEGRAM_API_TOKEN)

    @property
    def _message_text_handler(self):
        """
        Определяет обработчик для сообщения
        """
        if self._text[0] == '/':
            return command_handler
        elif self._text[0] == '-':
            return remove_handler
        elif self._text.isdigit() or self._text.lower() == 'вверх':
            return move_handler
        elif re.fullmatch(
                r'\s*\d+\s*{}\s*\d+\s*'.format(REPLACE_SEPARATOR), self._text):
            return replace_handler
        else:
            return add_handler

    def answer(self):
        """
        Передаёт сообщения в обработчик и отвечает
        """
        try:
            reply_text = self._message_text_handler(self._text, self._user)
        except Exception as exp:
            reply_text = 'Нажмите на /start'
            print(exp)
        self.bot.send_message(
            chat_id=self._chat_id, text=reply_text)
