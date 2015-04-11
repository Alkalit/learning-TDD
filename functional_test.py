import unittest
from selenium import webdriver

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

        # Он увидел что можно внести заметку

        # Он ввел "Купить сладкого хлеба" в текстовое поле
        # Когда он нажал ввод, страница обновилась, и на странице начался список:
        # "1: Купить сладкого хлеба" как элемент списка.

        # Окошко для ввдоа также было доступно
        # Пахом ввел:
        # "Накормить братишку". Пахом очень последователен
        # Страница снова обновилася и теперь на ней было видно два элемента списка:

        # Пахому стало интересно, сохранится ли список. И он заметил что сайт
        # сгенерировал для него уникальный урл. Этому способствовал пояснительный текст

        # Он перешел по этому урлу и его список дел был по прежднему там

        # Удовлетворенный, Пахом пошел спать.

if __name__ == '__main__':
    unittest.main(warnings='ignore')
