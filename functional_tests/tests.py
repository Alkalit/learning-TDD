from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class NewVisitorTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        # Неявно задать время ожидания до загрузки страницы
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_get_it_later(self):
        # Пахом зашел на главную страницу
        self.browser.get(self.live_server_url)

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

        # Когда он нажал ввод
        input_.send_keys(Keys.ENTER)
        # его перенесли на другой урл сайта
        pahom_list_url = self.browser.current_url
        self.assertRegex(pahom_list_url, '/lists/.+')

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
        self.browser.quit()

        # Новый пользователь, Братишка, зашел на сайт
        ## Мы используем новую сессию браузера чтобы убедиться что
        ## никакая информация об Пахоме не перешла через куки.
        self.browser = webdriver.Firefox()

        # Братишка зашел на домашнюю страницу. И не увидел ни следа от
        # списка Пахома
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('1: Купить сладкого хлеба', page_text)
        self.assertNotIn('2: Накормить братишку', page_text)

        # Братишка начал новый список, введя новую заметку.
        input_ = self.browser.find_element_by_id('new_item')
        input_.send_keys('Сорвать погону с поехавшего.')
        input_.send_keys(Keys.ENTER)

        # Братишка получил свой уникальный урл
        bratishka_list_url = self.browser.current_url
        self.assertRegex(bratishka_list_url, '/lists/.+')
        self.assertNotEqual(bratishka_list_url, pahom_list_url)

        # Удовлетворенный, Братишка тоже пошел спать

    def test_layout_and_styling(self):
        # Пахом зашел на домашнюю страницу
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)

        # Он отметил что форма ввода отцентрирована - ништяк!
        input_ = self.browser.find_element_by_id('new_item')
        self.assertAlmostEqual(
            input_.location['x'] + input_.size['width'] / 2, # центр инпута
            512,
            delta=5 # точность до 5 пикселей
        )

    def assertTODOInTable(self, todo_list_element):
        '''
        В книге обозначено как check_for_row_in_table
        Проверяет наличие элементов списка в таблице.
        Вынесено в отдельный метод из-за частого использования этого сниппета.
        '''

        table = self.browser.find_element_by_id('list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(todo_list_element, [row.text for row in rows])
