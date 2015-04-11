from django.test import TestCase
from django.core.urlresolvers import resolve
from django.http.request import HttpRequest
from django.template.loader import render_to_string

from lists.views import home_page


class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_returns_correct_html(self):
        request = HttpRequest()
        response = home_page(request)

        # Смотрим что нам пришла html-страница с нужным содержимым.
        expected_html = render_to_string('lists/home.html')
        self.assertEqual(response.content.decode(), expected_html)

    def test_can_save_a_POST_request(self):
        # Конструируем пост-запрос.
        request = HttpRequest()
        request.method = 'POST'
        request.POST['item_text'] = 'A new list item'

        response = home_page(request)

        self.assertIn('A new list item', response.content.decode())
        expected_html = render_to_string(
            'lists/home.html',
            {'new_item_text': 'A new list item'}
        )
        self.assertEqual(response.content.decode(), expected_html)
