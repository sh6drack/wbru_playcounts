import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By

data = pd.read_excel("test.xlsx", header=None)
driver = webdriver.Chrome()
driver.implicitly_wait(10)

for row in data.iterrows():
    title = row[1][0]
    url = row[1][1]
    driver.get(url)
    playcount = driver.find_element(By.CSS_SELECTOR, "span[data-testid='playcount']")
    print(f'{title}: {playcount.text}')

driver.quit()
