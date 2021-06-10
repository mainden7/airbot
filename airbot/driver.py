from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions


class WebDriver:
    class __WebDriver:
        def __init__(self):
            options = ChromeOptions()
            # options.add_argument('--disable-infobars')
            # options.add_argument('--disable-dev-shm-usage')
            # options.add_argument('--no-sandbox')
            options.add_argument("--start-maximized")
            options.add_argument("--remote-debugging-port=9222")
            self.driver = Chrome(options=options)

    driver = None

    def __init__(self):
        if not self.driver:
            WebDriver.driver = WebDriver.__WebDriver().driver
