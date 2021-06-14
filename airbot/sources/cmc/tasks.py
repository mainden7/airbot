import typing as ty
from airbot.tasks.base import BaseTask
from selenium.webdriver.remote.webelement import WebElement


class AddToWatchlistTask(BaseTask):
    """Click on button and add coin to CMC watchlist"""

    name = "Add to Watchlist"
    tags = ["watchlist", "add"]

    def __init__(
        self, element: WebElement, addresses: ty.Dict[str, str], **kwargs
    ):
        super().__init__(element, **kwargs)
        self.addresses = addresses

    def _get_key(self, text: str) -> str:
        """
        Get a value to input in address field based on given text hint.
        Determines which address we need to use from our list
        :param text:
        :return: str address
        """
        text = text.lower()
        if all(
            [
                "binance" in text,
                "smart" in text,
                "wallet" in text,
                "address" in text,
            ]
        ):
            key = self.addresses["bsc"]
        elif "ethereum" in text or "eth" in text:
            key = self.addresses["eth"]
        elif "tron" in text:
            key = self.addresses["tron"]
        else:
            raise ValueError

        return key

    def perform(self, modal) -> None:
        if self._element.text.strip() != "Done":
            self._element.click()

        input_ = modal.find_input(keywords=["address", "wallet"])
        if input_ and not input_.get_attribute("value"):
            input_.send_keys(
                self._get_key(input_.get_attribute("placeholder"))
            )
