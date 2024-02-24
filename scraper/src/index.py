from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import pandas as pd
from datetime import datetime
import locale
import os
from time import sleep


def gstaad_ticket_scraper(driver, wait, out_path):
    spinner_xpath = "//div[contains(@class, 'd-none') and @id='js-ticket-list-loading']"
    card_xpath = "//div[contains(@class, 'tickets-graph-swiper')]//div[@class='swiper-wrapper']//div[contains(@class, 'swiper-slide')]"
    price_xpath = "a[contains(@style, 'display:inline-block;')]"
    url = "https://gstaad.ticketcorner.ch/en/gstaad/ski-resort-2/ski-ticket?#js-anchor-ticket-list"

    driver.get(url)
    wait.until(lambda driver: driver.find_element(By.XPATH, spinner_xpath))
    elements = driver.find_elements(By.XPATH, card_xpath)
    df = pd.DataFrame(
        [
            [
                datetime.strptime(
                    e.get_attribute("data-date"),
                    "%Y-%m-%d",
                ),
                float(
                    e.find_element(By.XPATH, price_xpath).get_attribute("data-price")
                ),
            ]
            for e in elements
        ],
        columns=["date", "price"],
    )
    timestamp = datetime.now().isoformat()
    df["fetch_timestamp"] = timestamp
    df.to_csv(f"{out_path}/gstaad_{timestamp}.csv", index=False)
    print(df)
    return df


def scuol_ticket_scraper(driver, wait, out_path):
    full_month_xpath = "//div[contains(@class, 'dynamicPricing_container')]//button[contains(@class, 'btnSwitchMode')]"
    next_month_xpath = "//button[contains(@class, 'calendarSelector_navigation')][2]"
    card_xpath = "//div[contains(@class, 'dynamicPricing_cardContainer')]//div[contains(@class, 'weekRow')]//div[@class='itemContentDP_card ']"
    price_xpath = "div[contains(@class, 'itemContentDP_finalPrice')]"
    date_xpath = "div[contains(@class, 'itemContentDP_date')]"
    url = "https://shop.bergbahnen-scuol.ch/de/forfait-ski/1-tag-motta-naluns-dp"

    driver.get(url)
    driver.find_element(By.XPATH, full_month_xpath).click()

    month_count = 4 - datetime.now().month
    df = pd.DataFrame([], columns=["date", "price"]).dropna(axis=1, how="all")
    if month_count > 0:
        for _ in range(month_count + 1):
            elements = driver.find_elements(By.XPATH, card_xpath)
            df = pd.concat(
                [
                    df,
                    pd.DataFrame(
                        [
                            [
                                datetime.strptime(
                                    " ".join(
                                        [
                                            e.find_element(
                                                By.XPATH, date_xpath
                                            ).get_attribute("innerHTML"),
                                            "2024",
                                        ]
                                    ),
                                    "%d %B %Y",
                                ),
                                float(
                                    e.find_element(By.XPATH, price_xpath)
                                    .get_attribute("innerHTML")
                                    .replace(",", ".")
                                    .replace("&nbsp;CHF", "")
                                    .strip()
                                ),
                            ]
                            for e in elements
                        ],
                        columns=["date", "price"],
                    ),
                ],
                ignore_index=True,
            )
            driver.find_element(By.XPATH, next_month_xpath).click()
            sleep(2)
    timestamp = datetime.now().isoformat()
    df["fetch_timestamp"] = timestamp
    df.to_csv(f"{out_path}/scuol_{timestamp}.csv", index=False)
    print(df)
    return df


def main():
    locale.setlocale(locale.LC_TIME, "de_DE.UTF-8")
    driver_options = webdriver.FirefoxOptions()
    driver_options.add_argument("--headless")
    driver_options.add_argument("--disable-gpu")
    driver_options.add_argument("--no-sandbox")
    driver = webdriver.Firefox(options=driver_options)
    driver.set_window_position(0, 0)
    driver.set_window_size(1900, 1200)
    driver.implicitly_wait(5)
    wait = WebDriverWait(driver, 10)

    for scraper in [gstaad_ticket_scraper, scuol_ticket_scraper]:
        try:
            scraper(driver, wait, out_path=os.environ.get("OUT_PATH", "."))
        except Exception as e:
            print(e)

    driver.quit()


if __name__ == "__main__":
    main()
