import pandas as pd
import time
import os
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pandas as pd

# Chrome起動
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-notifications")
chrome_options.add_argument("--disable-popup-blocking")
chrome_options.add_argument("--load-extension=")
driver = webdriver.Chrome(options=chrome_options)
# アドレス
driver.get("https://fields.canpan.info/grant/index?page=4&sort=update&dir=desc")
# ページ全部リロードまで、5秒に待って
WebDriverWait(driver, 5)
print("page finished")
data = []
df = pd.DataFrame(data)
table=driver.find_element(By.ID,'search-results')
# divを探す
nndivs = table.find_elements(By.XPATH, "//div[@class='cell-wrapper first']")
print("found pages:",len(nndivs))
for i in range(len(nndivs)+2):
    try:
        link = table.find_element(By.XPATH, f"//*[@id='search-results']/table/tbody/tr[{i+2}]/td[1]/div/dl/dd[1]/h3/a")
    except Exception as e:
        print(e)
        break
    print(link.text)
    link.click()
    print("click")
    time.sleep(2)
    Ptable=driver.find_element(By.XPATH, "//*[@id='detail']/table")
    table_html = Ptable.get_attribute('outerHTML')
    df = pd.read_html(table_html)[0]
    df.to_excel(f'FR5/output{i+60}.xlsx', index=False)
    # 元のページに戻る
    driver.back()
    time.sleep(2)
