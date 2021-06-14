import typing as ty
from airbot.driver import WebDriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By


class PageElement:
    """
    A small wrapper around selenium WebElement that made to help with common
    tasks regarding this project
    Perhaps in future will be improved to fit more utility use cases

    Presumably all of our resources will be JS rendered web pages thus we made
    page elements validation with calling to WebDriverWait and expecting
    conditions checks by default.

    Args
        :param xpath: Xpath to corresponding page element
        :param css: CSS selector of this element, more efficient to provide css
        selector instead of an XPATH when required to load child HTML element
        from another page element.

        :param element: selenium WebElement
        :param time_: time to wait for element appears on page before throw
        `TimeoutException` error

    Any of xpath, css or element arguments must be provided
    """

    def __init__(
        self,
        xpath: str = None,
        css: str = None,
        element: WebElement = None,
        time_: float = 2.5,
    ):
        if not any([xpath, css, element]):
            raise ValueError(
                "Any of the arguments `xpath`, `css` or `element` is required."
                "  None provided"
            )

        self.css = css
        self.xpath = xpath
        self.time = time_

        self._element = element

        self.driver = WebDriver().driver

    @property
    def element(self) -> WebElement:
        """
        Construct selenium WebElement instance of corresponding html element
        here.
        Here we trying to guess what element we need so return only one. Must
        be provided strict css selector or xpath
        Using awaitable option by default as pages are JS rendered
        :return: WebElement

        :raises
            TimeoutException

        TODO: Add support of an option when page element is already
        constructed from selenium webelement
        """
        expr = (
            (By.XPATH, self.xpath)
            if self.xpath
            else (By.CSS_SELECTOR, self.css)
        )

        element = WebDriverWait(self.driver, self.time).until(
            expected_conditions.presence_of_element_located(expr)
        )

        return element

    @property
    def elements(self) -> ty.List[WebElement]:
        expr = (
            (By.XPATH, self.xpath)
            if self.xpath
            else (By.CSS_SELECTOR, self.css)
        )

        elements = WebDriverWait(self.driver, self.time).until(
            expected_conditions.presence_of_all_elements_located(expr)
        )

        return elements

    def __bool__(self) -> bool:
        """Checks for the presence of an element on the current page"""
        # TODO: Add reconstruct object option
        try:
            ele = self.element
            return True
        except TimeoutException:
            return False

    def find_child(self, css: str) -> WebElement:
        return self.element.find_element_by_css_selector(css)


class Notification(PageElement):
    """ """


class Button(PageElement):

    def click(self, scroll: bool = False) -> None:
        if scroll:
            self.driver.execute_script(
                "arguments[0].scrollIntoView();", self.element
            )
            self.driver.execute_script("arguments[0].click();", self.element)
        else:
            self.element.click()

    def is_active(self) -> bool:
        return not self.element.get_attribute("disabled") == "true"


class InputForm(PageElement):

    def __init__(
        self, submit: str = None, submit_xpath: str = None, *args, **kwargs
    ):
        assert any([submit, submit_xpath])

        super().__init__(*args, **kwargs)
        self._submit = submit
        self._submit_xpath = submit_xpath

    @property
    def submit(self) -> Button:
        # TODO: Improve this method. Make it found element not only by css
        if self._submit:
            element = self.element.find_element_by_css_selector(self._submit)
        else:
            element = self.element.find_element_by_xpath(self._submit_xpath)
        return element

    def _get_all_inputs(self) -> ty.List[WebElement]:
        return self.element.find_elements_by_tag_name("input")

    def is_valid(self) -> bool:
        # TODO: Find a way to validate forms
        return True
        # all_inputs = self._get_all_inputs()
        # return self.submit.is_active and all(
        #     [i.get_attribute("value") for i in all_inputs]
        # )

    def fill(self, fill_kw: ty.Dict[str, str], tag: str = "name"):
        for key, value in fill_kw.items():
            input_ = self.element.find_element_by_xpath(
                f"//input[@{tag}='{key}']"
            )
            input_.clear()
            input_.send_keys(value)

    def submit_form(self):
        for chk in self.element.find_elements_by_css_selector(
            "label.switch-label"
        ):
            self.driver.execute_script("arguments[0].scrollIntoView();", chk)
            self.driver.execute_script("arguments[0].click();", chk)

        if self.is_valid():
            self.submit.click()

    def fill_and_submit(
        self, fill_kw: ty.Dict[str, str], tag: str = "name"
    ) -> None:
        self.fill(tag=tag, fill_kw=fill_kw)
        self.submit_form()
