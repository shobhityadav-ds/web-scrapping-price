import time

import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

from utils import clean_price, ensure_data_dir, save_dataframe


def scrape_flipkart(max_pages=2, max_items=40):
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-notifications")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    products = []

    try:
        for page in range(1, max_pages + 1):
            url = f"https://www.flipkart.com/search?q=mobile+phones&page={page}"
            driver.get(url)

            try:
                close_button = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(normalize-space(), '✕') or contains(normalize-space(), 'X')]"))
                )
                close_button.click()
            except TimeoutException:
                pass

            time.sleep(4)
            driver.execute_script("window.scrollBy(0, 1200);")
            time.sleep(2)

            page_source = driver.page_source
            soup = BeautifulSoup(page_source, "html.parser")

            for card in soup.select("div.s0NCCf"):
                name_node = card.select_one("div.TbCaMn div")
                price_node = card.select_one("div.hZ3P6w.KTtanE")

                if not name_node or not price_node:
                    continue

                name = name_node.get_text(" ", strip=True)
                name = name.split(". ", 1)[-1].strip()
                price = clean_price(price_node.get_text(" ", strip=True))

                if not name or price is None:
                    continue

                products.append({
                    "Name": name,
                    "Price": price,
                    "Source": "Flipkart",
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
    save_dataframe(df, data_dir / "flipkart_products")
    return df
