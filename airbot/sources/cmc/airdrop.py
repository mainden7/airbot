import typing as ty
from airbot.driver import WebDriver
from airbot.tasks.base import BaseTask

from airbot.providers.telegram import Telegram
from airbot.providers.twitter import Twitter

from airbot.sources.cmc.elements import _joinAirdropButton
from airbot.sources.cmc.elements import _joinAirdropModal


from selenium.webdriver.remote.webelement import WebElement


class Airdrop:
    """
    Main interface of airdrops from coinmarketcap

    Args
        :param name: str - Airdrop name
        :param url: str - link to corresponding page on CMC
        :param twitter: Twitter - twitter provider with defined auth
        credentials
        :param telegram: Telegram - telegram provider with defined auth
        credentials
        :param addresses: dict with addresses where reward will be send if you
        have enough luck as CMC airdrops is a kind of lottery
    """

    def __init__(
        self,
        name: str,
        url: str,
        twitter: Twitter,
        telegram: Telegram,
        addresses: ty.Dict[str, str],
    ):
        self.name = name
        self.url = url

        self.driver = WebDriver().driver
        self.twitter = twitter
        self.telegram = telegram
        self.addresses = addresses

        self.tasks = []
        self.done_tasks = []

    def __eq__(self, other) -> bool:
        """
        Checks if other airdrop is the same as self. Main airdrops identity
        comparison tool. Will be upgraded to more robust in future as compare
        only names at the moment
        :param other: Airdrop instance
        :return: bool
        """
        return self.name == other.name

    def _load(self) -> None:
        """
        Loads airdrop home page.
        :return: None
        """
        self.driver.get(self.url)

    def _translate(self):
        # TODO: Add switch region
        pass

    def _make_task(self, element: WebElement) -> BaseTask:
        """
        Attempt to make a task instance from given html element.

        :param element: selenium WebElement
        :return: one of the BaseTask inherited objects
        """
        text = element.text.lower()
        btn = element.find_element_by_css_selector("button")

        task = BaseTask.make_from_raw_text(
            text=text,
            element=btn,
            addresses=self.addresses,
            twitter=self.twitter,
            telegram=self.telegram,
        )
        if task:
            self.tasks.append(task)
        return task

    def _build_tasks(self) -> None:
        """
        Search for all html elements that look alike tasks and build
        corresponding objects from them.
        :return: None
        """
        divs = _joinAirdropModal.get_task_divs()
        for div in divs:
            self._make_task(div)

    def _process_tasks(self) -> None:
        """
        Iterate through all the found tasks and calls task execution method to
        perform that task. Mark it as done when completed
        :return: None
        TODO: Add tasks exception handle
        """
        for task in self.tasks:
            task.perform(_joinAirdropModal)
            self.done_tasks.append(task)

    def find_tasks(self, keyword: str) -> ty.List[BaseTask]:
        """
        Finds the tasks which tags match given keyword. Draft realization.
        Probably will be replaced with more efficient method.
        :param keyword: str
        :return: list of tasks or empty list matched given keyword
        """
        tasks = []
        for task in self.tasks:
            if keyword in task.tags:
                tasks.append(task)
        return tasks

    def participate(self) -> None:
        """
        Start point of participating in airdrop.
        :return: None
        """
        self._load()
        _joinAirdropButton.click(True)
        self._build_tasks()
        self._process_tasks()
        _joinAirdropModal.submit_form()
