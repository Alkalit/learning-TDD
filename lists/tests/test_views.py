from django.test import TestCase
from django.core.urlresolvers import resolve
from django.http.request import HttpRequest
from django.template.loader import render_to_string

from lists.views import home_page
from lists.models import Item, List


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


class ListViewTest(TestCase):

    def test_uses_list_template(self):
        list_ = List.objects.create()
        response = self.client.get('/lists/%d/' % list_.id)
        self.assertTemplateUsed(response, 'lists/list.html')

    def test_displays_all_items_for_current_list(self):
        correct_list = List.objects.create()
        Item.objects.create(text='item 1', list=correct_list)
        Item.objects.create(text='item 2', list=correct_list)
        other_list = List.objects.create()
        Item.objects.create(text='Other item 1', list=other_list)
        Item.objects.create(text='Other item 2', list=other_list)

        response = self.client.get('/lists/%d/' % correct_list.id)

        self.assertContains(response, 'item 1')
        self.assertContains(response, 'item 2')
        self.assertNotContains(response, 'Other item 1')
        self.assertNotContains(response, 'Other item 2')

    def test_saving_a_POST_request(self):
        ## test_saving_a_POST_request и test_redirects_after_POST
        ## разделены чтобы было проще выявлять работу вьюхи.
        # item_text - ключ который присылает форма.
        self.client.post(
            '/lists/new',
            data={'item_text': 'A new list item'}
        )

        # Проверяем что она сохранила значение заметки
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

    def test_redirects_after_POST(self):
        response = self.client.post(
            '/lists/new',
            data={'item_text': 'A new list item'}
        )

        list_ = List.objects.first()

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/lists/%d/' % list_.id)

    def test_passes_correct_list_to_template(self):
        correct_list = List.objects.create()
        other_list = List.objects.create()

        response = self.client.get('/lists/%d/' % correct_list.id, )

        self.assertEqual(response.context['list'], correct_list)

class NewItemTest(TestCase):

    def test_can_save_POST_request_to_an_existing_list(self):
        correct_list = List.objects.create()
        other_list = List.objects.create()

        self.client.post(
            '/lists/%d/add_item' % correct_list.id,
            data={'item_text': 'A new item for an existing list'}
        )

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new item for an existing list')
        self.assertEqual(new_item.list, correct_list)

    def test_redirects_to_list_view(self):
        correct_list = List.objects.create()
        other_list = List.objects.create()

        response = self.client.post(
            '/lists/%d/add_item' % correct_list.id,
            data={'item_text': 'A new item for an existing list'}
        )

        self.assertRedirects(response, '/lists/%d/' % correct_list.id)