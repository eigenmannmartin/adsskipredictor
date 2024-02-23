from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

def main(url, spinner_xpath, card_xpath, price_xpath):
    driver_options = webdriver.FirefoxOptions()
    driver_options.add_argument("--headless")
    driver_options.add_argument("--disable-gpu")
    driver_options.add_argument("--window-size=1024,768")
    driver_options.add_argument("--no-sandbox")

    driver = webdriver.Firefox(options=driver_options)
    driver.implicitly_wait(30)
    driver.get(url)
    wait = WebDriverWait(driver, 10)
    wait.until(lambda driver: driver.find_element(By.XPATH, spinner_xpath))
    elements = driver.find_elements(By.XPATH, card_xpath)
    print([(e.get_attribute('aria-label'), e.get_attribute('data-date'), e.find_element(By.XPATH, price_xpath).get_attribute("data-price")) for e in elements])

    driver.quit()

spinner_xpath = "//div[contains(@class, 'd-none') and @id='js-ticket-list-loading']"
card_xpath = "//div[contains(@class, 'tickets-graph-swiper')]//div[@class='swiper-wrapper']//div[contains(@class, 'swiper-slide')]"
price_xpath = "//a[contains(@style, 'display:inline-block;')]"
url = "https://gstaad.ticketcorner.ch/en/gstaad/ski-resort-2/ski-ticket?#js-anchor-ticket-list"
main(url, spinner_xpath, card_xpath, price_xpath)