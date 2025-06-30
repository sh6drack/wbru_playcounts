import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By

data = pd.read_excel("data.xlsx", header=None)
options = webdriver.ChromeOptions()
# options.add_argument('headless')
driver = webdriver.Chrome(options=options)
driver.implicitly_wait(10)

playcounts = []

for row in data.iterrows():
    url = row[1][0]
    if str(url).startswith(("https://open.spotify.com/track/", "http://open.spotify.com/track/")):
        driver.get(url)
        playcount_element = driver.find_element(By.CSS_SELECTOR, "span[data-testid='playcount']")
        count = int(playcount_element.text.replace(",", ""))
        count_in_millions = count/1_000_000
        playcounts.append(count_in_millions)
    else:
        playcounts.append("")

data['Playcounts'] = playcounts
data.to_excel("data.xlsx", header=None, index=False)

driver.quit()
