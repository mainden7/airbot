from airbot.tasks.base import BaseTask
from selenium.webdriver.remote.webelement import WebElement


class TwitterBaseTask(BaseTask):
    def __init__(self, twitter, element: WebElement, *args, **kwargs):
        super().__init__(*args, **kwargs)
        link = element.find_element_by_css_selector("a").get_attribute("href")

        self.twitter = twitter
        self.link = link

    def perform(self, modal) -> None:
        """ """


class FollowTwitterTask(TwitterBaseTask):
    name = "Follow Twitter"
    tags = ["twitter", "follow"]

    def perform(self, modal) -> None:
        self.twitter.follow(self.link)
        input_ = modal.find_input(keywords=["twitter", "handle"])
        if input_ and not input_.get_attribute("value"):
            input_.send_keys(self.twitter.name)


class RetweetTask(TwitterBaseTask):
    name = "Retweet"
    tags = ["retweet"]

    def perform(self, modal) -> None:
        link = self.twitter.retweet(self.link)
        input_ = modal.find_input(keywords=["retweeted", "post"])
        if input_ and not input_.get_attribute("value"):
            input_.send_keys(link)
