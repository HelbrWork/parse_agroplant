import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


df_urls = pd.read_excel('links.xlsx')


options = webdriver.ChromeOptions()
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)

# Установите явные ожидания
wait = WebDriverWait(driver, 20)


data_list = []


for index, row in df_urls.iterrows():
    url = row['URL']
    driver.get(url)

    try:

        product_name = wait.until(EC.presence_of_element_located((By.XPATH, "//h1"))).text


        try:
            price_element = driver.find_element(By.XPATH, "//meta[@property='product:price:amount']")
            price = price_element.get_attribute("content")
        except:
            price = "Price not available"


        try:
            description_element = driver.find_element(By.XPATH, "//meta[@property='og:description']")
            description = description_element.get_attribute("content")
        except:
            description = "Description not available"


        data_list.append({
            "URL": url,
            "Product Name": product_name,
            "Price": price,
            "Description": description
        })

    except Exception as e:
        print(f"Error parsing {url}: {e}")
        driver.save_screenshot(f"screenshot_{index}.png")

    time.sleep(2)


df_parsed = pd.DataFrame(data_list)
df_parsed.to_csv("parsed_data.csv", index=False)


driver.quit()
