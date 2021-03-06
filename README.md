-- Репо книги: https://github.com/hjwp/book-example

-- ПРЕДИСЛОВИЕ:
    The reason is that a to-do list is a really nice example. At its most basic it is very simple
    indeed — just a list of text strings — so it's easy to get a "minimum viable" list app up and
    running. But it can be extended in all sorts of ways—different persistence models,
    adding deadlines, reminders, sharing with other users, and improving the client-side
    UI. There's no reason to be limited to just "to-do" lists either; they could be any kind of
    lists. But the point is that it should allow me to demonstrate all of the main aspects of
    web programming, and how you apply TDD to them.

    Ultimately, programming is hard. Often, we are smart, so we succeed. TDD is there to
    help us out when we’re not so smart. Kent Beck (who basically invented TDD) uses the
    metaphor of lifting a bucket of water out of a well with a rope: when the well isn’t too
    deep, and the bucket isn’t very full, it’s easy. And even lifting a full bucket is pretty easy
    at first. But after a while, you’re going to get tired. TDD is like having a ratchet that lets
    you save your progress, take a break, and make sure you never slip backwards. That way
    you don’t have to be smart allthe time.



-- По селениуму:
    -- При первых же проблемах всегда старайся обновиться.
    -- Селениуму нужен абсолютный урл для перехода на страницу.
        self.browser.get(self.live_server_url)
    -- При переходе на другой урл просто меняется состояние объекта browser. Ничего отлавливать не надо.

        # Когда он нажал ввод
        input_.send_keys(Keys.ENTER)
        # его перенесли на другой урл сайта
        pahom_list_url = self.browser.current_url

    -- Имеет смысл создавать свои специфицеские ассерты чтобы уменьшить количество вводимого кода.
        def assertTODOInTable(self, to_list_element):
            '''
            В книге обозначено как check_for_row_in_table
            Проверяет наличие элементов списка в таблице.
            Вынесено в отдельный метод из-за частого использования этого сниппета.
            '''

            table = self.browser.find_element_by_id('list_table')
            rows = table.find_elements_by_tag_name('tr')
            self.assertIn(to_list_element, [row.text for row in rows])

    -- LiveServerTestCase expects to be run by the Django test runner using manage.py. As
        of Django 1.6, the test runner will find any files whose name begins with test. To keep
        things neat and tidy, let's make a folder for our functional tests, so that it looks a bit like
        an app. All Django needs is for it to be a valid Python module (ie, one with a  __in‐
        it__.pyin it):

        -- В принципе код функциональных тестов может распологаться и пакетах приложений проекта. Но т.к. они тестируют все приложение целиком и т.к. юзеру
            все равно где какое приложение, в этом нет необходимости. Поэтому лучше держать такие тесты в одельном пакете.

    -- Для запуска функциональных тестов на отдельном сервере их надо отнаследовать от LiveServerTestCase и 
        запускать через manage test


-- ГЛОБАЛЬНЫЕ ПРИМЕЧАНИЯ:
    -- По книге шаблона находятся в папках каждого приложения.
    -- Автор придерживается конвенции о том что урлы не заканчивающиеся на слеш изменяют данные.

-- Функциональные тесты так называются потому что они позволяют оценить приложение с точки зрения функционирования пользователя.
    -- Терминология: Functional Test == Acceptance Test == End-to-End Test
        -- Это все одно и  то же.

-- Рабочий процесс при TDD:
    -- Сначала пишется функциональный тест, описывающий работу приложения с точки зрения пользователя.
    -- Как только будет готов падающий тест, мы начинаем думать над кодом который может его пройти. Или хотя бы текущую ошибку в тесте.
        С этого момента пишится один или более юниттестов, которые определяют как мы хотим чтобы на код себя вел. Идея в том чтобы каждая строка кода была 
        проверена хотя бы одним тестом.
    -- Как только у нас будут падающие тесты, мы пишем самый маленький кусочек рабочего кода, достаточный чтобы пройти юниттест.
    -- Шаг 2 и 3 можно проходить несколько раз, до тех пор пока функциональные тесты, как нам кажется, не продвинутся.
    -- Теперь можно перезапустить функциональные тесты и посмотреть прошли ли они или хотя бы продвинулись дальше. Это может сподвигнуть написать новые юниттест.
        И новый код и так далее.

    -- Итого:
        """
        Functional  tests  should  help  you  build  an  application  with  the  right
        functionality,  and  guarantee  you  never  accidentally  break  it.  Unit  tests
        should help you to write code that's clean and bug free.
        """

-- Каждый раз когда написав кусок кода, после которого ты считаешь себя умным, стоит обеспокоиться. Потому что вероятно получившийся код избыточно сложен.
-- Three Strikes and Refactor:
    -- Если код повторяется трижды, это плохой признак. Значит нужен рефакторинг.
-- Перед рефакторингом всегда делай коммит.
-- Интеграционные тесты отличаются от юнитовых тем что вторые проверяют только логику приложения. Первые же при этом еще могут работать с БД и другими данными.

-- TDD is closely associated with the agile movement in software development, which
    includes a reaction against  Big Design Up Frontthe traditional software engineering
    practice whereby, after a lengthy requirements gathering exercise, there is an equally
    lengthy design stage where the software is planned out on paper. The agile philosophy
    is that you learn more from solving problems in practice than in theory, especially when
    you confront your application with real users as soon as possible.
    Instead of a long upfront design phase, we try and put a minimum viable application  out there early, and let
    the design evolve gradually based on feedback from real-world usage.

-- YAGNI!
    Once you start thinking about design, it can be hard to stop. All sorts of other thoughts
    are occurring to us—we might want to give each list a name or title, we might want to
    recognise users using usernames and passwords, we might want to add a longer notes
    field as well as short descriptions to our list, we might want to store some kind of or‐
    dering, and so on. But we obey another tenet of the agile gospel: “YAGNI” (pronounced
    yag-knee), which stands for “You aint gonna need it!” As software developers, we have
    fun creating things, and sometimes it's hard to resist the urge to build things just because
    an idea occurred to us and we mightneed it. The trouble is that more often than not,
    no matter how cool the idea was, you won'tend up using it. Instead you have a load of
    unused code, adding to the complexity of your application. YAGNI is the mantra we
    use to resist our overenthusiastic creative urges.

-- REST
    We have an idea of the data structure we want—the Model part of Model-View-Controller (MVC).
    What about the View and Controller parts? How should the user interact with Lists and their Items using a web browser?

    Representational State Transfer (REST) is an approach to web design that's usually used to guide the design of web-based APIs.
    When designing a user-facing site, it's not possible to stick strictly to the REST rules, but they still provide some useful inspiration.

    REST suggests that we have a URL structure that matches our data structure, in this case lists and list items. Each list can have its own URL:

        /lists/<list identifier>/

    That will fulfill the requirement we've specified in our FT. To view a list, we use a GET request (a normal browser visit to the page).

    To create a brand new list, we'll have a special URL that accepts POST requests:

        /lists/new

    To add a new item to an existing list, we'll have a separate URL, to which we can send POST requests:

        /lists/<list identifier>/add_item

    (Again, we're not trying to perfectly follow the rules of REST, which would use a PUT request here—we're just using REST for inspiration.)

-- КОНЦЕПЦИИ:
    -- User Story
        -- A description of how the application will work from the point of view of the user.  Used to structure a functional test.
    -- Regression
        -- When new code breaks some aspect of the application which used to work.
    -- Unexpected failure
        -- When a test fails in a way we weren't expecting. This either means that we've made
        a mistake in our tests, or that the tests have helped us find a regression, and we need
        to fix something in our code.
    -- Red/Green/Refactor
        -- Another way of describing the TDD process. Write a test and see it fail (Red), write
        some code to get it to pass (Green), then Refactor to improve the implementation.
    -- Triangulation
        -- Adding a test case with a new specific example for some existing code, to justify
        generalising the implementation (which may be a "cheat" until that point).
    -- Three strikes and refactor
        -- A rule of thumb for when to remove duplication from code. When two pieces of
        code look very similar, it often pays to wait until you see a third use case, so that
        you're more sure about what part of the code really is the common, re-usable part
        to refactor out.
    -- The scratchpad to-do list
        -- A place to write down things that occur to us as we're coding, so that we can finish up what we're doing and come back to them later.
    -- Итеративность разработки:
        -- Писать код последовательно шаг за шагом в соответствии с методологией и тестами. И ни в коем случае не пытаться реализовать все изменения за раз.
            -- Скажем мы хотим чтобы для каждого пользователя создвался отдельный уникальный урл с его списком дел. А текущее приложение не имеет такой возможности.
                Т.е. нам нужно решение для n количества списков, а в данный момент доступно для 0. Но решение для 1го (best-url-ever/) тоже хорошее начало.
