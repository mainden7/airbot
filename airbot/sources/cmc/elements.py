import typing as ty

from airbot.html import Button
from airbot.html import InputForm
from airbot.html import Notification

from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import NoSuchElementException


class AirdropForm(InputForm):
    """
    Coinmarketcap airdrop participate main form, opened in modal.

    """

    def get_divs(self, role: str) -> ty.List[WebElement]:
        """
        Gets all divs of parent element that has child element of a given
        role
        :param role: str - css selector
        :return: list of selenium WebElement objects
        """
        divs = self.element.find_elements_by_css_selector("div")
        result_divs = []
        for div in divs:
            try:
                div.find_element_by_css_selector("div")
                continue
            except NoSuchElementException:
                pass

            try:
                div.find_element_by_css_selector(role)
                result_divs.append(div)
            except NoSuchElementException:
                pass

        return result_divs

    def get_task_divs(self) -> ty.List[WebElement]:
        """
        Retrieve all the divs from self with the buttons inside.
        It may be interpreted as a task
        :return: list of selenium WebElements
        """
        task_divs = self.get_divs(role="button")
        # return all except last as it is submit form button
        # and we do not need it
        return task_divs[:-1]

    def get_input_divs(self) -> ty.List[WebElement]:
        """
        Retrieve all the divs from self element with the inputs inside.
        It may be interpreted as form fileds where we need to enter
        corresponding info to get reward
        :return: list of selenium WebElements objects
        """
        input_divs = self.get_divs(role="input")
        return input_divs

    def find_input(self, keywords: ty.List[str]) -> WebElement:
        """
        Returns input WebElement that math given keywords
        :param keywords: list of strings
        :return: WebElement
        """
        for div in self.get_input_divs():
            input_ = div.find_element_by_css_selector("input")
            if all(
                [
                    k in input_.get_attribute("placeholder").lower()
                    for k in keywords
                ]
            ):
                return input_


_loginButton = Button(
    xpath="//button[text()='Log In']",
    css="button.x0o17e-0:nth-child(4)",
)
_loginModal = InputForm(
    xpath="//div[contains(@class, 'modalWrpper___2ibHA')]",
    css="div.modalWrpper___2ibHA",
    submit="button",
)
_profileButton = Button(
    xpath="//button[contains(@class, 'cmc-profile-popover__trigger')]",
    css="button.cmc-profile-popover__trigger",
)
_successLoginNotification = Notification(
    xpath="//div[text()='You have successfully logged in!']",
)
_joinAirdropButton = Button(
    xpath="//button[contains(., 'Join')]",
)
_joinAirdropModal = AirdropForm(
    xpath="//div[contains(@class, 'modalWrpper___2ibHA')]",
    css="div.modalWrpper___2ibHA ",
    submit="button",
)
