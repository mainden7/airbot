from airbot.sources.cmc import CMC
from tests.conftest import BaseTestClass
from airbot.driver import WebDriver


class TestCMC(BaseTestClass):
    page = None

    @classmethod
    def setup_class(cls):
        super().setup_class()
        root_url = cls.config["sources"]["cmc"]

        cmc = CMC(
            root_url=root_url,
            credentials=dict(
                email=cls.config["cmc"]["login"],
                password=cls.config["cmc"]["password"],
            ),
        )
        cmc.driver = WebDriver().driver

        cls.page = cmc
        cls.page.root_page_load()

    @classmethod
    def teardown_class(cls):
        cls.page.driver.quit()

    def test_login(self):
        assert not self.page.logged_in
        self.page.login()
        assert self.page.logged_in
