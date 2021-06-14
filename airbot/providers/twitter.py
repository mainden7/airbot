import time
import typing as ty
from contextlib import contextmanager

from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from airbot.html import Button
from airbot.html import PageElement
from airbot.html import InputForm
from airbot.html import Notification

from airbot.driver import WebDriver

_loginButton = Button(xpath="//a[@href = '/login']")
_profileBox = PageElement(
    xpath="//div[@data-testid='SideNav_AccountSwitcher_Button']"
)
_loginForm = InputForm(
    xpath="//form[@action='/sessions']",
    css="form",
    submit_xpath="//div[@data-testid='LoginForm_Login_Button']",
)
_followButton = Button(xpath="//div[@data-testid='placementTracking']")
_retweetButton = Button(xpath="//div[@data-testid='retweet']")
_quoteRetweetButton = Button(xpath="//a[@href='/compose/tweet']")
_submitQuoteTweetButton = Button(xpath="//div[@data-testid='tweetButton']")
_successNotification = Notification(xpath="//div[@data-testid='toast']")


class Twitter:
    """
    General interface to perform twitter related tasks.

    Args
        :param name: twitter profile name. Must starts with `@`
        :param email: twitter email used to login
        :param password: raw twitter password
    """

    def __init__(self, name: str, email: str, password: str):
        self.name = name
        self.email = email
        self.password = password

    def __login_send_keys(self, send_email: bool = True) -> None:
        """
        Fill login form with twitter credentials. Use twitter name instead of
        email when twitter complains with too much login activity and asks to
        fill one more login form

        :param send_email: if true then use email used upon registration,
        uses twitter name otherwise
        :return: None
        """
        login = self.email if send_email else self.name
        _loginForm.fill_and_submit(
            fill_kw={
                "session[username_or_email]": login,
                "session[password]": self.password,
            }
        )

    def _login(self) -> None:
        """
        Performs login into twitter action. Handles one case of
        an unusual twitter activity blockage
        :return: None
        """
        driver = WebDriver().driver
        try:
            _loginButton.click()
            time.sleep(2)
        except TimeoutException as e:
            if _profileBox:
                return
            else:
                raise e

        if "Login on Twitter" in driver.title:
            self.__login_send_keys()
            try:
                # tracking an unusual twitter activity blockage
                driver.find_element_by_xpath(
                    "//input[@name='session[username_or_email]']"
                )
            except NoSuchElementException:
                return

            self.__login_send_keys(send_email=False)

    @contextmanager
    def open_session(self, link: str) -> ty.Iterator[None]:
        """
        As all twitter activity should be performed when logged in so we wraps
        all of them with this contextmanager that do all routine stuff such as
        account login, tabs management and twitter redirects

        Support after login redirect to home page instead of staying on the
        provided one

        :param link: Page link where all of the required actions should be made
        :return: Iterator
        """
        driver = WebDriver().driver
        driver.execute_script(f"window.open('{link}','_blank');")

        WebDriverWait(driver, 2).until(
            expected_conditions.number_of_windows_to_be(2)
        )

        all_tabs = driver.window_handles
        parent_tab = driver.window_handles[0]
        new_tab = [x for x in all_tabs if x != parent_tab][0]

        driver.switch_to.window(new_tab)

        self._login()

        if "/home" in driver.current_url:
            # TODO: add support of all redirects and not only to home page
            # sometimes logins automatically and redirects to home page
            driver.get(link)

        yield
        time.sleep(1)
        driver.close()
        driver.switch_to.window(parent_tab)

    def follow(self, link: str) -> None:
        """
        Follows twitter account. Should be provided the link to that account
        :param link:
        :return: None
        """
        with self.open_session(link):
            if _followButton.element.text.lower() == "follow":
                _followButton.click()

    def retweet(self, link: str) -> str:
        """
        Performs a quoted retweet of the given post. Also keep track of
        produced tweet and returns a link to it.
        :param link: link to the page with required post
        :return: (str) - link to retweeted post

        TODO: Get rid of sleeps
        """
        driver = WebDriver().driver
        with self.open_session(link):
            time.sleep(2)
            _retweetButton.click()
            _quoteRetweetButton.click()
            time.sleep(2)
            driver.switch_to.active_element.send_keys("Awesome project!")
            _submitQuoteTweetButton.click()
            if _successNotification:
                _successNotification.element.find_element_by_css_selector("a")
                href = (
                    _successNotification.element.find_element_by_css_selector(
                        "a"
                    ).get_attribute("href")
                )
                return href
