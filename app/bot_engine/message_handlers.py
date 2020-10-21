import re
import bot_engine.database_handler as database_handler
from bot_engine.utils import (clear_add_data, clear_remove_data,
                              UserFullResponse)
from bot_engine.request_makers import (create_user, add_elements,
                                       replace_element, remove_elements,
                                       get_all, make_request)
from bot_engine.messages import WELCOME_TEXT, HELP_TEXT


VALID_COMMANDS = ['/start', '/help']


def command_handler(text, user, *args, **kwargs):
    """
    Обработчик команд
    """
    if text not in VALID_COMMANDS:
        return ('Команда {} не предусмотрена, попробуйте одну из этих {}'
                .format(text, ', '.join(VALID_COMMANDS)))
    elif text == '/start':
        new_user = database_handler.create_user(user.id)
        if new_user:
            make_request(create_user(
                user.id, user.first_name, user.last_name, user.username))
        full_info = UserFullResponse(make_request(get_all(user.id)))
        return WELCOME_TEXT + full_info.show()
    else:
        return HELP_TEXT


def move_handler(text, user, *args, **kwargs):
    """
    Обработчик перемещения по спискам
    """
    new_position = int(text.lower().replace('вверх', '0'))
    full_info = UserFullResponse(make_request(get_all(user.id)))
    if new_position == 0:
        database_handler.change_user_position(user.id, 0)
        return full_info.show()
    else:
        try:
            current_list = full_info.get_list(new_position)
            database_handler.change_user_position(user.id, new_position)
            return current_list.show()
        except IndexError:
            return ('Отсутствует список под номером {}.\n\n'
                    .format(new_position) + full_info.show())


def replace_handler(text, user, *args, **kwargs):
    """
    Обработчик перемещения элементов
    """
    movable_element, new_ind = [int(n) for n in re.findall(r'\d+', text)]
    position = database_handler.get_user_position(user.id)
    make_request(replace_element(user.id, position, movable_element, new_ind))
    full_info = UserFullResponse(make_request(get_all(user.id)))
    if position == 0:
        return full_info.show()
    else:
        return full_info.get_list(position).show()


def remove_handler(text, user, *args, **kwargs):
    """
    Обработчик удаления элементов
    """
    elements_to_remove = clear_remove_data(text)
    position = database_handler.get_user_position(user.id)
    make_request(remove_elements(
        user.id, position, elements_to_remove), answer=False)
    full_info = UserFullResponse(make_request(get_all(user.id)))
    if position == 0:
        return full_info.show()
    else:
        return full_info.get_list(position).show()


def add_handler(text, user, *args, **kwargs):
    """
    Обработчик добавления элементов
    """
    elements_to_add = clear_add_data(text)
    position = database_handler.get_user_position(user.id)
    make_request(add_elements(
        user.id, position, elements_to_add))
    full_info = UserFullResponse(make_request(get_all(user.id)))
    if position == 0:
        return full_info.show()
    else:
        return full_info.get_list(position).show()
