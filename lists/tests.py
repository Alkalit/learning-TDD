from django.test import TestCase
from django.core.urlresolvers import resolve
from django.http.request import HttpRequest
from django.template.loader import render_to_string

from lists.views import home_page
from lists.models import Item


class HomePageTest(TestCase):

    def test_saves_items_only_when_necessary(self):
        request = HttpRequest()
        response = home_page(request)

        self.assertEqual(Item.objects.all(), 0)

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
        note = 'A new list item'
        # Конструируем пост-запрос.
        request = HttpRequest()
        request.method = 'POST'
        # item_text - ключ который присылает форма.
        request.POST['item_text'] = note

        # Отправляем запрос вьюхе
        response = home_page(request)

        # Проверяем что она сохранила значение заметки
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, note)

        self.assertIn('A new list item', response.content.decode())
        expected_html = render_to_string(
            'lists/home.html',
            {'new_item_text': note}
        )

        self.assertEqual(response.content.decode(), expected_html)

class ItemModelTest(TestCase):

    def test_saving_and_retrieving_items(self):
        first_item = Item()
        first_item.text = 'The first (ever) list item'
        first_item.save()

        second_item = Item()
        second_item.text = 'The second item'
        second_item.save()

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]

        self.assertEqual(first_saved_item.text, 'The first (ever) list item')
        self.assertEqual(second_saved_item.text, 'The second item')
