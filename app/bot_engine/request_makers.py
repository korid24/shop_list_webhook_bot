import json
import requests
from typing import List, NamedTuple, Optional, Union
from config import AUTH_TOKEN, BASE_URL
# from local_utils import write_json
from bot_engine.utils import path_to

HEADERS = {
    'Content-type': 'application/json',
    'Authorization': 'token {}'.format(AUTH_TOKEN),
    'Accept-Language': 'en-US'}


class RequestConstructor(NamedTuple):
    """
    Шаблон для информации запроса
    """
    url: str
    method: str
    data: Optional[Union[list, dict]]


def create_user(
        telegram_id: int,
        first_name: Optional[str],
        last_name: Optional[str],
        nickname: Optional[str]) -> RequestConstructor:
    """
    Формирует информацию для запроса на добавление пользоавателя
    """
    data = {
        'telegram_id': telegram_id,
        'first_name': first_name,
        'last_name': last_name,
        'nickname': nickname}
    url = BASE_URL + path_to('user')
    return RequestConstructor(url=url, data=data, method='post')


def add_elements(
        telegram_id: int,
        position: int,
        elements: List[str]) -> RequestConstructor:
    """
    Формирует информацию для запроса на добавление элемента
    """
    data = []
    for element in elements:
        data.append({'title': element})
    if position:
        url = (BASE_URL + path_to('user', telegram_id) +
               path_to('purchaselist', position) +
               path_to('purchase') + 'bulk_create/')
    else:
        url = (BASE_URL + path_to('user', telegram_id) +
               path_to('purchaselist') + 'bulk_create/')
    return RequestConstructor(url=url, data=data, method='post')


def replace_element(
        telegram_id: int,
        position: int,
        old_ind: int,
        new_ind: int) -> RequestConstructor:
    """
    Формирует информацию для запроса на перемещение элемента
    """
    data = {'ind': new_ind}
    if position:
        url = (BASE_URL + path_to('user', telegram_id) +
               path_to('purchaselist', position) +
               path_to('purchase', old_ind))
    else:
        url = (BASE_URL + path_to('user', telegram_id) +
               path_to('purchaselist', old_ind))
    return RequestConstructor(url=url, data=data, method='patch')


def remove_elements(
        telegram_id: int,
        position: int,
        elements: List[int]) -> RequestConstructor:
    """
    Формирует информацию для запроса на удаление элемента
    """
    data = {'items': elements}
    if position:
        url = (BASE_URL + path_to('user', telegram_id) +
               path_to('purchaselist', position) +
               path_to('purchase') + 'bulk_delete/')
    else:
        url = (BASE_URL + path_to('user', telegram_id) +
               path_to('purchaselist') + 'bulk_delete/')
    return RequestConstructor(url=url, data=data, method='delete')


def get_all(telegram_id: int) -> RequestConstructor:
    """
    Формирует информацию для запроса на получение полной инфы о пользователе
    """
    url = BASE_URL + path_to('user', telegram_id)
    return RequestConstructor(url=url, data=None, method='get')


def make_request(
        info: RequestConstructor, answer: bool = True) -> Union[dict, int]:
    """
    Совершает запрос исходя из предоставленной инфы. Возвращает тело ответа
    если нужно, а если не нужно то код ответа
    """
    response = requests.request(
        method=info.method,
        url=info.url,
        data=json.dumps(info.data),
        headers=HEADERS)
    if not answer:
        return response.status_code
    return response.json()
