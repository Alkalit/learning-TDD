from .base import FunctionalTest

class ItemValidationTest(FunctionalTest):

    def test_cannot_add_empty_item(self):
        # Пахом зашел на домашнюю страницу и случайно нажал ввод при пустом поле
        # ввода
        self.browser.get(self.server_url)
        self.get_item_input_box().send_keys('\n')


        # Страница обновилась и появилось сообщение об ошибке, говорящее о том
        # что тудушка не может быть пустой
        error = self.browser.find_element_by_css_selector('.has-error')
        self.assertEqual(error.text, "You can't have an empty list item")

        # Он попробовал ввести какой-нибудь текст для проверки и теперь он
        # добавился
        self.get_item_input_box().send_keys('Сочинить песню про слоника\n')
        self.assertTODOInTable('1: Сочинить песню про слоника')

        # Намеренно, он теперь решил ввести пустой ввод еще раз.
        self.get_item_input_box().send_keys('\n')

        # Сообщение об ошибке появилось снова.
        self.assertTODOInTable('1: Сочинить песню про слоника')
        error = self.browser.find_element_by_css_selector('.has-error')
        self.assertEqual(error.text, "You can't have an empty list item")

        # И он исправил это введя новую тудушку.
        self.get_item_input_box().send_keys('Приготовить сладкого хлеба\n')
        self.assertTODOInTable('1: Сочинить песню про слоника')
        self.assertTODOInTable('2: Приготовить сладкого хлеба')
