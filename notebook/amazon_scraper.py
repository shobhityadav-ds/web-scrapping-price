import time

import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from utils import clean_price, ensure_data_dir, save_dataframe


def scrape_amazon(max_pages=2, max_items=40):
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36")

    driver = webdriver.Chrome(options=options)
    products = []

    try:
        for page in range(1, max_pages + 1):
            url = f"https://www.amazon.in/s?k=mobile+phones&page={page}"
            driver.get(url)

            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-component-type='s-search-result']"))
            )
            time.sleep(2)

            soup = BeautifulSoup(driver.page_source, "html.parser")
            items = soup.select("div[data-component-type='s-search-result']")

            for item in items:
                title_node = item.select_one("h2 span")
                price_node = item.select_one("span.a-price-whole")

                if not title_node or not price_node:
                    continue

                price = clean_price(price_node.get_text(" ", strip=True))
                if price is None:
                    continue

                products.append({
                    "Name": title_node.get_text(" ", strip=True),
                    "Price": price,
                    "Source": "Amazon",
                    "Page": page,
                })

                if len(products) >= max_items:
                    break

            if len(products) >= max_items:
                break
    finally:
        driver.quit()

    df = pd.DataFrame(products).drop_duplicates(subset=["Name"])
    data_dir = ensure_data_dir()
    save_dataframe(df, data_dir / "amazon_products")
    return df
