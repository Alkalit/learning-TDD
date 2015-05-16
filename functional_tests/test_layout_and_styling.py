from .base import FunctionalTest

class LayoutAndStylingTest(FunctionalTest):

    def test_layout_and_styling(self):
        # Пахом зашел на домашнюю страницу
        self.browser.get(self.server_url)
        self.browser.set_window_size(1024, 768)

        # Он отметил что форма ввода отцентрирована - ништяк!
        input_ = self.browser.find_element_by_id('new_item')
        self.assertAlmostEqual(
            input_.location['x'] + input_.size['width'] / 2, # центр инпута
            512,
            delta=10 # точность до 10 пикселей
        )

        # Он начал новый список и отметил что он тоже отцентрирован
        input_.send_keys('testing\n')
        input_ = self.browser.find_element_by_id('new_item')
        self.assertAlmostEqual(
            input_.location['x'] + input_.size['width'] / 2, # центр инпута
            512,
            delta=10 # точность до 10 пикселей
        )
