from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from scrapers import (
    adelboden_ticket_scraper,
    gstaad_ticket_scraper,
    scuol_ticket_scraper,
    pizol_ticket_scraper,
)
import locale
import os
import sentry_sdk
from sentry_sdk.crons import monitor

sentry_sdk.init(
    dsn=os.environ.get("SENTRY_DSN", ""),
    traces_sample_rate=float(os.environ.get("SENTRY_TRACES_RATE", "0.0")),
    profiles_sample_rate=float(os.environ.get("SENTRY_PROFILE_RATE", "0.0")),
)


@monitor(monitor_slug="scrape")
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

    for scraper in [
        adelboden_ticket_scraper,
        pizol_ticket_scraper,
        gstaad_ticket_scraper,
        scuol_ticket_scraper,
    ]:
        try:
            with sentry_sdk.start_transaction(op="scrape", name=scraper.__name__):
                scraper(driver, wait, out_path=os.environ.get("OUT_PATH", "."))
        except Exception as e:
            sentry_sdk.capture_exception(e)

    driver.quit()


if __name__ == "__main__":
    main()
