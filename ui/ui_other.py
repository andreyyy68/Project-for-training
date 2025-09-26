from playwright.sync_api import expect

def test_text_box_form(page):

        # Открыть страницу
        page.goto("https://demoqa.com/text-box")

        # --- разные варианты локаторов ---

        # 1. По id
        page.fill("#userName", "Анна Иванова")

        # 2. По placeholder
        page.fill("input[placeholder='name@example.com']", "anna@test.com")

        # 3. По type
        page.fill("textarea#currentAddress", "Москва, ул. Ленина, 1")

        # 4. По role + name (лучший способ для кнопок)
        page.get_by_role("button", name="Submit").click()

        # 5. По text (альтернативный способ кликнуть кнопку)
        page.click("text=Submit")


def test_checkbox(page):
        page.goto('https://demoqa.com/checkbox')

        # Раскрываем все узлы
        page.locator("button[title='Expand all']").click()

        # Чекбоксы по порядку
        checkboxes = [
            "home", "desktop", "notes", "commands", "documents",
            "workspace", "react", "angular", "veu", "office",
            "public", "private", "classified", "general", "downloads",
            "wordFile", "excelFile"
        ]

        # Проставляем галочки
        for cb in checkboxes:
            page.locator(f"label[for='tree-node-{cb}'] span.rct-checkbox").check()

        # Проверяем результат
        result_text = page.locator("#result").inner_text()
        for cb in checkboxes:
            assert cb in result_text, f"{cb} не найден в результате"

def test_radio_button(page):
    page.goto('https://demoqa.com/radio-button')

# Локаторы
    yes_radio = page.locator("#yesRadio")
    impressive_radio = page.locator("#impressiveRadio")
    no_radio = page.locator("#noRadio")

    # Проверяем, что кнопки видимы
    expect(yes_radio).to_be_visible()
    expect(impressive_radio).to_be_visible()
    expect(no_radio).to_be_visible()

    # Кликаем по label для "Yes"
    page.locator("label[for='yesRadio']").click()
    expect(yes_radio).to_be_checked()
    expect(page.locator(".text-success")).to_have_text("Yes")

    # Кликаем по label для "Impressive"
    page.locator("label[for='impressiveRadio']").click()
    expect(impressive_radio).to_be_checked()
    expect(page.locator(".text-success")).to_have_text("Impressive")

    # Проверяем, что "No" задизейблен
    expect(no_radio).to_be_disabled()

def test_click(page):
    page.goto('https://demoqa.com/buttons')

    dbl_click = page.locator("#doubleClickBtn")
    right_click = page.locator("#rightClickBtn")
    one_click = page.get_by_text("Click Me", exact=True) # Здесь мы используеем exact, чтобы найти точное совпадение по тексту

    dbl_click.dblclick()
    right_click.click(button="right")
    one_click.click()

    expect(page.locator("#doubleClickMessage")).to_have_text("You have done a double click")
    expect(page.locator("#rightClickMessage")).to_have_text("You have done a right click")
    expect(page.locator("#dynamicClickMessage")).to_have_text("You have done a dynamic click")

def test_download_file(page, tmp_path):

    page.goto("https://demoqa.com/upload-download")

    # Создаём временный файл для загрузки
    file_path = tmp_path / "demoqa_test_file.txt"
    file_path.write_text("Hello, this is a test file for DemoQA upload!")

    # Загружаем файл
    page.set_input_files("#uploadFile", str(file_path))

    # Проверяем, что имя файла отобразилось на странице
    uploaded_file_name = page.locator("#uploadedFilePath")
    assert file_path.name in uploaded_file_name.inner_text()

def test_dynamic_element(page):
    page.goto("https://demoqa.com/dynamic-properties")
    # --- Кнопка, которая появляется через 5 секунд ---
    dynamic_btn = page.locator("#visibleAfter")

    # Ждём, пока кнопка станет видимой
    expect(dynamic_btn).to_be_visible(timeout=6000)  # таймаут чуть больше 5 секунд

    # Кликаем после того, как она появилась
    dynamic_btn.click()

    # --- Кнопка, которая активна через 5 секунд ---
    enable_btn = page.locator("#enableAfter")
    expect(enable_btn).to_be_enabled(timeout=6000)
    enable_btn.click()

def handle_alert(dialog):
    dialog.accept()  # принимаем alert

def test_simple_alert(page):
    page.goto("https://demoqa.com/alerts")

    # Подписываемся на простой alert
    def handle_alert(dialog):
        assert dialog.message == "You clicked a button"
        dialog.accept()

    page.once("dialog", handle_alert)
    page.locator("#alertButton").click()

def test_timer_alert(page):
    page.goto("https://demoqa.com/alerts")

    # Alert появляется через 5 секунд
    def handle_alert(dialog):
        assert dialog.message == "This alert appeared after 5 seconds"
        dialog.accept()

    page.once("dialog", handle_alert)
    page.locator("#timerAlertButton").click()


def test_confirm_alert(page):
    page.goto("https://demoqa.com/alerts")

    # Подтверждаем confirm (OK)
    def handle_confirm(dialog):
        assert dialog.message == "Do you confirm action?"
        dialog.accept()  # можно dialog.dismiss() для Cancel

    page.once("dialog", handle_confirm)
    page.locator("#confirmButton").click()


def test_prompt_alert(page):
    page.goto("https://demoqa.com/alerts")

    # Вводим текст в prompt
    def handle_prompt(dialog):
        assert dialog.message == "Please enter your name"
        dialog.accept("Playwright User")  # текст для prompt

    page.once("dialog", handle_prompt)
    page.locator("#promptButton").click()

    # Проверяем, что текст отобразился на странице
    output = page.locator("#promptResult").inner_text()
    assert "Playwright User" in output

def test_date_picker_select_option(page):
    page.goto("https://demoqa.com/date-picker")

    # Локатор поля даты
    date_input = page.locator("#datePickerMonthYearInput")
    date_input.click()  # открываем календарь

    # Выбираем месяц и год через select_option
    page.locator(".react-datepicker__month-select").select_option("7")  # август (0-based)
    page.locator(".react-datepicker__year-select").select_option("2025")  # год

    # Выбираем день (например, 25-е число)
    page.locator(".react-datepicker__day--025").click()

    # Проверяем, что значение инпута изменилось
    assert date_input.input_value() == "08/25/2025"

def test_date_and_time_picker(page):
    page.goto("https://demoqa.com/date-picker")

    # Находим поле Date and Time
    dt_input = page.locator("#dateAndTimePickerInput")
    dt_input.click()

    # --- Выбираем месяц ---
    page.locator(".react-datepicker__month-read-view").click()
    page.locator(".react-datepicker__month-option >> text=August").click()

    # --- Выбираем год ---
    page.locator(".react-datepicker__year-read-view").click()
    page.locator(".react-datepicker__year-option >> text=2025").click()

    # --- Выбираем день ---
    page.locator(".react-datepicker__day--008").click()  # 8 число

    # --- Выбираем время ---
    page.locator(".react-datepicker__time-list-item >> text=10:00").click()

    # Проверяем, что поле обновилось
    value = dt_input.input_value()  # берём текущее значение поля
    assert value == "August 8, 2025 10:00 AM"

def test_automation_practice_form_stable_complete(page):
    page.goto("https://demoqa.com/automation-practice-form")

    # Заполняем имя и фамилию
    page.get_by_placeholder("First Name").fill("Andrew")
    page.get_by_placeholder("Last Name").fill("U")

    # Заполняем почту
    page.get_by_placeholder("name@example.com").fill("theBest@example.com")

    # Выставляем гендер
    page.locator("label[for='gender-radio-2']").click(force=True)

    # Заполняем номер телефона
    page.get_by_placeholder("Mobile Number").fill("888888889")

    # Проставляем дату
    date_input = page.locator("#dateOfBirthInput")
    date_input.click()
    page.locator(".react-datepicker__month-select").select_option("7")
    page.locator(".react-datepicker__year-select").select_option("2025")
    page.locator(".react-datepicker__day--008:not(.react-datepicker__day--outside-month)").click()
    assert "08 Aug 2025" in date_input.input_value()

    # Заполняем предмет
    subjects_input = page.locator("#subjectsInput")
    subjects_input.fill("Maths")

    # Выбираем хобби
    page.locator("label[for='hobbies-checkbox-1']").click(force=True)


    # Пишем адрес
    page.get_by_placeholder("Current Address").fill("123 Test Street")

    # Выбираем штат
    page.locator("#state").click()
    page.locator("div[id^='react-select-3-option']:has-text('NCR')").click()

    # Выбираем город
    page.locator("#city").click()
    page.locator("div[id^='react-select-4-option']:has-text('Delhi')").click()

    # Жмем на "Submit"
    page.locator("#submit").click(force=True)





