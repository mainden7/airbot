import typing as ty
from abc import ABCMeta
from abc import abstractmethod
from airbot.driver import WebDriver
from airbot.providers.telegram import Telegram
from airbot.providers.twitter import Twitter


class AirdropSource(metaclass=ABCMeta):
    """
    : currently in develop mode
    Airdrop source base class. Should be instantiated by all new airdrop
    sources.

    """

    def __init__(
        self,
        root_url: str,
        twitter: Twitter,
        telegram: Telegram,
        addresses: ty.Dict[str, str],
        credentials: ty.Dict[str, ty.Union[str, str]],
    ):
        self.driver = None
        self.root_url = root_url

        self.twitter = twitter
        self.telegram = telegram
        self.addresses = addresses

        self.credentials = credentials
        self.logged_in = False

    def root_page_load(self):
        """Loads the root page """
        self.driver.get(self.root_url)

    def __enter__(self):
        self.driver = WebDriver().driver
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.driver.quit()

    @abstractmethod
    def process(self, config):
        pass

    @abstractmethod
    def login(self, **credentials) -> None:
        pass

    @abstractmethod
    def get_ongoing_airdrops(self) -> ty.List:
        pass

    @abstractmethod
    def get_participated_airdrops(self) -> ty.List:
        pass
