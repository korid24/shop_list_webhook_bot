# Shop list bot
Бот для ведения списков покупок
Репозиторий с сервисом, через который работает этот бот:
https://github.com/korid24/shop_list_via_django

Находясь в меню списков можно выполнить следующие дейсвия:
1. Создать новые списки, для этого необходимо просто ввести желаемое название \
(или названия через запятую или перенос строки) и список(и) сразу появится в перечне.
2. Удалять списки, для этого нужно написать \'-\', а затем порядковый номер(а) \
списка(ов). К примеру, сообщение -2 удалит список под номером 2 вместе с содержимым.
3. Перейти в список, для этого нужно написать порядковый номер списка.
к примеру, сообщение 1 перенесёт вас в список под номером 1.
4. Переместить список. Сообщение \'7//3\' переместит список на под номером 7 на место номер 3

Находясь внутри списка можно выполнять следующие действия:
1. Добавлять покупки, для этого нужно ввести название покупки и она появится в списке, \
либо названия нескольких покупок через запятую или перенос строки
2. Удалять покупки, для этого нужно написать \'-\', а затем порядковый номер покупки. \
Сообщение -2 удалит покупку под номером 2, сообщение -1,3,6 удалит покупки под \
соответствующими номерами, а сообщение -1-5 удалит покупки с первой по пятую.
3. Перейти к перечню списков, для этого в меню списка необходимо ввести вверх или 0
4. Перемещать покупки по аналогии со списками


[Перейти в бота](https://t.me/shop_assistant_list_bot)
либо найти по имени @shop_assistant_list_bot
