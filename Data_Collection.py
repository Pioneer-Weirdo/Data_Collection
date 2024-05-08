import json
import random

from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from tqdm import tqdm


def Login_operation():
    # Chromedriver的路径
    chromedriver_path = r"Driver/chromedriver-win64/chromedriver.exe"

    # 配置Chrome选项
    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = r"Driver/chrome-win64/chrome.exe"

    # 启动Chrome浏览器
    driver = webdriver.Chrome(executable_path=chromedriver_path, options=chrome_options)

    # 打开网址
    driver.get("https://www.fenqubiao.com/Default.aspx")

    # 找到搜索框并输入关键词
    username = driver.find_element(By.ID, 'Username')
    username.send_keys("zzuli")
    password = driver.find_element(By.ID, 'Password')
    password.send_keys("zzuli")
    submit = driver.find_element(By.ID, 'login_button')
    submit.click()

    # 等待搜索结果加载
    time.sleep(5)
    # 获取页面源码
    link = driver.find_element(By.XPATH, "//a[@href='/Connect/NewVersion.aspx']")
    link.click()
    link = driver.find_element(By.XPATH, "//a[@href='/Macro/Journal?name=计算机科学']")
    link.click()
    return driver


original_data = []


def get_Collection(driver: WebDriver, url):
    global partition
    driver.get(url)
    random_wait_time = random.randint(1, 3)
    driver.implicitly_wait(random_wait_time)  # 等待10秒钟，可以根据实际情况调整
    journal_info_element = driver.find_element(By.CLASS_NAME, "box-body")

    # 提取期刊信息
    journal_info = {}
    rows = journal_info_element.find_elements(By.TAG_NAME, "tr")

    td_elements = journal_info_element.find_elements(By.TAG_NAME, "td")

    # 遍历每个 td 元素
    for td in td_elements:
        # 在当前 td 元素下查找所有的 span 元素
        span_elements = td.find_elements(By.TAG_NAME, "span")

        # 如果存在 span 元素
        if span_elements:
            # 遍历每个 span 元素，获取其 class 值
            partition = []
            for span in span_elements:
                class_value = span.get_attribute("class")
                # javascript
                script = f"""
                return window.getComputedStyle(document.querySelector('span.{class_value}'), '::before').getPropertyValue('content');
                """
                pseudo_element_content = driver.execute_script(script)
                partition.append(pseudo_element_content)
                # 输出伪元素内容
                # print("td 下存在 span，class 值为:", class_value, "::before 伪元素内容:", pseudo_element_content)
            break  # 如果找到了 span 元素，则跳出循环
    journal_info['分区'] = partition
    for row in rows:
        columns = row.find_elements(By.TAG_NAME, "td")
        key = columns[0].text.strip()
        value = columns[1].text.strip()
        journal_info[key] = value

    original_data.append(journal_info)
    # 输出期刊信息
    # print(journal_info)


if __name__ == '__main__':
    driver = Login_operation()
    with open('links.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    for idx, (link, journal) in tqdm(enumerate(data.items()), total=len(data), desc="Processing links"):
        print(link, journal)
        get_Collection(driver, link)
        if idx % 50 == 0:
            name = int(idx / 50)
            with open('data/data{}.json'.format(name), 'w', encoding='utf-8') as f:
                json.dump(original_data, f, ensure_ascii=False, indent=4)
            # 重置original_data,每50条重置一次,防止占用内存
            original_data = []
