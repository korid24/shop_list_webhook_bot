from typing import List, Optional
import re


def open_range(r: str) -> List[int]:
    """
    Преобразует интервал переданные в запросе на удаление в список чисел,
    входящих в этот интервал
    """
    start, finish = r.split('-')
    return range(int(start), int(finish)+1)


def clear_remove_data(data: str) -> List[int]:
    """
    Преобразует запрос на удаление в список чисел
    """
    data = (re.findall(r'\d+-\d+|\d+', data))
    clear_data = []
    for element in data:
        if element.isdigit():
            clear_data.append(int(element))
        else:
            clear_data += open_range(element)
    return sorted(set(clear_data))


def clear_add_data(data: str) -> List[str]:
    """
    Преобразует запрос на добаление в список строк
    """
    data = re.sub(r' +', ' ', data.strip())
    data = re.sub(r'Список .+:\n', '', data)
    data = [item.strip() for item in re.split(
        r'\n|\,|\d+\.', data) if item.strip()]
    set_of_data = set(data)
    if len(data) == len(set_of_data):
        return [element.capitalize() for element in data]
    else:
        clear_data = []
        for element in data:
            if element in set_of_data:
                set_of_data.remove(element)
                clear_data.append(element)
                if not set_of_data:
                    break
        return [element.capitalize() for element in clear_data]


def path_to(destination: str, key: Optional[int] = None) -> str:
    """
    Генерирует часть url с путем до пользователя, списка или покупки
    """
    valid_destinations = ['user', 'purchaselist', 'purchase']
    if destination not in valid_destinations:
        raise KeyError('destination must be {}'.format(
            ' or '.join(valid_destinations)))
    path = 'bot_{}/'.format(destination)
    if key:
        path += str(key) + '/'
    return path


class PurchaseList:
    """
    Интерпретация списока пользователя в виде объекта
    """
    def __init__(self, info: dict):
        self.title = info.get('title')
        self.ind = info.get('ind')
        self.items_to_show = [(item['ind'], item['title'])
                              for item in info.get('items', [])]

    def _show_items(self) -> str:
        output = []
        if not self.items_to_show:
            return 'Здесь пусто. Чтобы добавить элемент, напишите его название'
        for ind, title in self.items_to_show:
            output.append('{}. {}'.format(str(ind), title))
        return '\n'.join(output)

    def get_header(self) -> str:
        return 'Список {}:\n\n'.format(self.title)

    def show(self):
        return self.get_header() + self._show_items()


class UserFullResponse(PurchaseList):
    """
    Интерпретация информации о пользователе, полученной в ответ
    на запрос в виде объекта
    """
    def __init__(self, info: dict):
        super(UserFullResponse, self).__init__(info)
        self.accost = info.get('first_name') or info.get('nickname')
        self.lists = [PurchaseList(item) for item in info.get('items', [])]

    def get_header(self) -> str:
        if self.accost:
            return '{}, вот ваши списки:\n\n'.format(self.accost)
        return 'Перечень ваших списков:\n\n'

    def get_list(self, key: int) -> PurchaseList:
        return self.lists[key-1]
