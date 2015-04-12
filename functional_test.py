import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_get_it_later(self):
        # Пахом зашел на главную страницу
        self.browser.get('http://localhost:8000')

        # И обратил внимание на заголовок в браузере
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # Он увидел что можно внести заметку
        input_ = self.browser.find_element_by_id('new_item')
        self.assertEqual(
            input_.get_attribute('placeholder'),
            'Введите заметку'
        )

        # Он ввел "Купить сладкого хлеба" в текстовое поле
        input_.send_keys('Купить сладкого хлеба')

        # Когда он нажал ввод, страница обновилась,
        input_.send_keys(Keys.ENTER)

        # и на странице начался список:
        # "1: Купить сладкого хлеба" как элемент списка.
        self.assertTODOInTable('1: Купить сладкого хлеба')

        # Окошко для ввдоа также было доступно
        # Пахом ввел:
        # "Накормить братишку". Пахом очень последователен
        input_ = self.browser.find_element_by_id('new_item')
        input_.send_keys('Накормить братишку')
        input_.send_keys(Keys.ENTER)

        # Страница снова обновилася и теперь на ней было видно два элемента списка:
        self.assertTODOInTable('1: Купить сладкого хлеба')
        self.assertTODOInTable('2: Накормить братишку')

        # Пахому стало интересно, сохранится ли список. И он заметил что сайт
        # сгенерировал для него уникальный урл. Этому способствовал пояснительный текст

        # Он перешел по этому урлу и его список дел был по прежднему там

        # Удовлетворенный, Пахом пошел спать.

    def assertTODOInTable(self, to_list_element):
        '''
        В книге обозначено как check_for_row_in_table
        Проверяет наличие элементов списка в таблице.
        Вынесено в отдельный метод из-за частого использования этого сниппета..
        '''

        table = self.browser.find_element_by_id('list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(to_list_element, [row.text for row in rows])

if __name__ == '__main__':
    unittest.main(warnings='ignore')
