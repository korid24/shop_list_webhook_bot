import re
from unittest import TestCase, main
from bot_engine import request_makers
from config import BASE_URL


class RequestMakersTest(TestCase):
    def test_create_user(self):
        request = request_makers.create_user(12345, 'ivan', 'petrov', 'ninja')
        self.assertTrue(
            isinstance(request, request_makers.RequestConstructor))
        self.assertEqual('post', request.method)

    def test_add_elements_data(self):
        request = request_makers.add_elements(
            telegram_id=123456,
            position=1,
            elements=['Milk', 'Cheese', 'Butter'])
        self.assertEqual(request.method, 'post')
        self.assertEqual(
         request.data,
         [
             {'title': 'Milk'},
             {'title': 'Cheese'},
             {'title': 'Butter'}])

    def test_add_purchases_url(self):
        request = request_makers.add_elements(
            telegram_id=123456,
            position=1,
            elements=['Milk', 'Cheese', 'Butter'])
        self.assertEqual(
            request.url,
            re.sub(r'\s', '',
                   BASE_URL +
                   '''
                   bot_user/123456/bot_purchaselist/1/bot_purchase/bulk_create/
                   '''))

    def test_add_lists_url(self):
        request = request_makers.add_elements(
            telegram_id=123456, position=0, elements=['products', 'birthday'])
        self.assertEqual(
            request.url,
            re.sub(r'\s', '',
                   BASE_URL +
                   '''
                   bot_user/123456/bot_purchaselist/bulk_create/
                   '''))

    def test_replace_element_data(self):
        request = request_makers.replace_element(
            telegram_id=123456,
            position=0,
            old_ind=2,
            new_ind=6)
        self.assertEqual(request.method, 'patch')
        self.assertEqual(request.data, {'ind': 6})

    def test_replace_purchase_url(self):
        request = request_makers.replace_element(
            telegram_id=123456,
            position=1,
            old_ind=2,
            new_ind=6)
        self.assertEqual(
            request.url,
            re.sub(r'\s', '',
                   BASE_URL +
                   '''
                   bot_user/123456/bot_purchaselist/1/bot_purchase/2/
                   '''))

    def test_replace_list_url(self):
        request = request_makers.replace_element(
            telegram_id=123456,
            position=0,
            old_ind=2,
            new_ind=6)
        self.assertEqual(
            request.url,
            re.sub(r'\s', '',
                   BASE_URL +
                   '''
                   bot_user/123456/bot_purchaselist/2/
                   '''))

    def test_remove_data(self):
        request = request_makers.remove_elements(
            telegram_id=123456,
            position=0,
            elements=[1, 4])
        self.assertEqual(request.method, 'delete')
        self.assertEqual(request.data, {'items': [1, 4]})

    def test_remove_purchases_url(self):
        request = request_makers.remove_elements(
            telegram_id=123456,
            position=2,
            elements=[1, 4])
        self.assertEqual(
            request.url,
            re.sub(r'\s', '',
                   BASE_URL +
                   '''
                   bot_user/123456/bot_purchaselist/2/bot_purchase/bulk_delete/
                   '''))

    def test_remove_lists_url(self):
        request = request_makers.remove_elements(
            telegram_id=123456,
            position=0,
            elements=[1, 4])
        self.assertEqual(
            request.url,
            re.sub(r'\s', '',
                   BASE_URL +
                   '''
                   bot_user/123456/bot_purchaselist/bulk_delete/
                   '''))

    def test_get_all(self):
        request = request_makers.get_all(telegram_id=123456)
        self.assertEqual(request.url, BASE_URL + 'bot_user/123456/')
        self.assertEqual(request.data, None)
        self.assertEqual(request.method, 'get')


if __name__ == '__main__':
    main()
