from django.test import TestCase
from django.core.exceptions import ValidationError

from lists.models import Item, List


class ListModelTest(TestCase):

    def test_get_absolute_url(self):
        list_ = List.objects.create()
        self.assertEqual(list_.get_absolute_url(), '/lists/%d/' % list_.id)


class ItemModelTest(TestCase):

    def test_default_text(self):
        item = Item()
        self.assertEqual(item.text, '')

    def test_item_is_related_to_list(self):
        list_ = List.objects.create()
        item = Item.objects.create(list=list_)

        self.assertIn(item, list_.item_set.all())

    def test_string_representation(self):
        item = Item(text='some text')

        self.assertEqual(str(item), 'some text')

    def test_list_ordering(self):
        list_ = List.objects.create()

        item1 = Item.objects.create(list=list_, text='i1')
        item2 = Item.objects.create(list=list_, text='item 2')
        item3 = Item.objects.create(list=list_, text='third')

        self.assertEqual(
            list(Item.objects.all()),
            [item1, item2, item3]
        )

    def test_duplicate_items_are_invalid(self):
        list_ = List.objects.create()
        Item.objects.create(list=list_, text='spam')

        with self.assertRaises(ValidationError):
            item = Item(list=list_, text='spam')
            item.full_clean()

    def test_CAN_save_same_item_to_differ_list(self):
        '''
        Дополнительный тест имеющий отношение к test_duplicate_items_are_invalid.
        '''
        some_list = List.objects.create()
        Item.objects.create(list=some_list, text='spam')

        other_list = List.objects.create()
        item = Item(list=other_list, text='spam')
        item.full_clean()  # should not raise

    def test_cannot_save_empty_list_item(self):
        list_ = List.objects.create()
        item = Item(list=list_, text='')

        with self.assertRaises(ValidationError):
            item.save()
            item.full_clean() # Принудительно вызвать полную валидацию данных полей.
