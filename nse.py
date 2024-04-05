from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
import time
import requests
import pandas as pd
# Создаем объект настроек Chrome
options = webdriver.ChromeOptions()

# Устанавливаем прокси-сервер
# proxy_server_url = "154.236.179.226"
# options.add_argument(f'--proxy-server={proxy_server_url}')

# Создаем экземпляр веб-драйвера с опциями
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

# Открываем сайт
driver.get("https://www.nseindia.com")

time.sleep(20)

# Найдем элемент "Market" с помощью XPath
market_element = driver.find_element(By.XPATH, "/html/body/header/nav/div[2]/div/div/ul/li[3]/a")

# Создаем объект ActionChains
actions = ActionChains(driver)

# Наведем мышь на элемент "Market"
actions.move_to_element(market_element)
actions.pause(2)  # Добавляем задержку в 2 секунды

# Найдем элемент, по которому нужно кликнуть после "Market" с помощью XPath
sub_element_xpath = "/html/body/header/nav/div[2]/div/div/ul/li[3]/div/div[1]/div/div[1]/ul/li[1]/a"
sub_element = driver.find_element(By.XPATH, sub_element_xpath)

# Кликнем по найденному элементу после "Market"
actions.click(sub_element)

# Выполним все действия
actions.perform()

# Ждем, пока элемент выбора загрузится
select_element = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, "/html/body/div[11]/div/section/div/div/div/div/div/div/div[2]/div[1]/div[1]/div[2]/select"))
)

# Создаем объект Select
select = Select(select_element)

# Выбираем опцию по индексу (в данном случае, шестую опцию)
option_index = 5
selected_option = select.options[option_index]
selected_option_text = selected_option.text

# Нажимаем на выбранную опцию
select_element.click()

# Ждем, чтобы список опций появился
time.sleep(1)

# Находим опцию по тексту и кликаем на нее
option_xpath = f"//option[text()='{selected_option_text}']"
option_element = driver.find_element(By.XPATH, option_xpath)
option_element.click()

time.sleep(15)

# Ждем, пока таблица загрузится
table_xpath = "/html/body/div[11]/div/section/div/div/div/div/div/div/div[3]/div/table"
table_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, table_xpath)))

# Получаем HTML-код таблицы
table_html = table_element.get_attribute('outerHTML')

# Используем pandas для парсинга HTML и создания DataFrame
df = pd.read_html(table_html)[0]

# Сохраняем DataFrame в CSV файл
df.to_csv('table_data.csv', index=False)

# Закрываем драйвер
driver.quit()
