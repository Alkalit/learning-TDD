from django.test import TestCase
from django.core.urlresolvers import resolve
from django.http.request import HttpRequest
from django.template.loader import render_to_string

from lists.views import home_page


class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = home_page(request)

        # Проверка содержимого страницы
        # Смотрим что нам пришла html-страница с нужным содержимым.
        self.assertTrue(response.content.startswith(b'<html>'))
        self.assertIn(b'<title>To-Do list</title>', response.content)
        # стрип нужен из символа \n в конце файла
        self.assertTrue(response.content.strip().endswith(b'</html>'))
