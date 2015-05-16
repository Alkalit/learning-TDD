import sys

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver


class FunctionalTest(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls): # setUpClass исполняется единожды перед запуском тестового класса
        '''
        Если тесты запущены с заданным доменным именем, то использовать его.
        Иначе использовать обычную тестовую конфигурацию (localhost:8081).
        https://docs.djangoproject.com/en/1.8/topics/testing/tools/#django.test.LiveServerTestCase
        '''
        for arg in sys.argv:
            if 'liveserver' in arg:
                cls.server_url = 'http://' + arg.split('=')[1]
                return # прекратить исполнение метода.

        super().setUpClass()
        cls.server_url = cls.live_server_url

    @classmethod
    def tearDownClass(cls):
        if cls.server_url == cls.server_url:
            super().tearDownClass()

    def setUp(self):
        self.browser = webdriver.Firefox()
        # Неявно задать время ожидания до загрузки страницы
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.refresh() # for WinError 10054
        self.browser.quit()

    def assertTODOInTable(self, todo_list_element):
        '''
        В книге обозначено как check_for_row_in_table
        Проверяет наличие элементов списка в таблице.
        Вынесено в отдельный метод из-за частого использования этого сниппета.
        '''

        table = self.browser.find_element_by_id('list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(todo_list_element, [row.text for row in rows])
