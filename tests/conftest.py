import configparser



class BaseTestClass:
    config = None
    driver = None

    @classmethod
    def setup_class(cls):
        config = configparser.ConfigParser()
        config.read("./config.ini")

        cls.config = config
        # options = ChromeOptions()
        # # options.add_argument('headless')
        # # options.add_argument('--disable-infobars')
        # # options.add_argument('--disable-dev-shm-usage')
        # # options.add_argument('--no-sandbox')
        # options.add_argument("--start-maximized")
        # options.add_argument("--remote-debugging-port=9222")
        # cls.driver = Chrome(options=options)


