from airbot.tasks.base import BaseTask
from airbot.providers.telegram import Telegram
from selenium.webdriver.remote.webelement import WebElement


class JoinTelegramGroupTask(BaseTask):
    name = "Join Telegram Channel"
    tags = ["join", "telegram", "channel"]

    def __init__(self, element: WebElement, telegram: Telegram, **kwargs):
        super().__init__(element, **kwargs)
        link = element.find_element_by_css_selector("a").get_attribute("href")
        self.telegram = telegram
        self.link = link

    def perform(self, modal) -> None:
        self.telegram.join_group(self.link)

        input_ = modal.find_input(keywords=["telegram", "handle"])
        if input_ and not input_.get_attribute("value"):
            input_.send_keys(self.telegram.name)
