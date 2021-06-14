import os
import re
import typing as ty

from airbot.sources.base import AirdropSource

from airbot.sources.cmc.airdrop import Airdrop
from airbot.sources.cmc.elements import _loginModal
from airbot.sources.cmc.elements import _loginButton
from airbot.sources.cmc.elements import _profileButton
from airbot.sources.cmc.elements import _successLoginNotification


class CMC(AirdropSource):
    """
    Coinmarketcap crypto source https://coinmarketcap.com/
    """

    @staticmethod
    def _is_successfully_logged_in() -> bool:
        """
        Checks if the notification of success login appeared or profile
        button persist on current page, that may be indicated as logged IN
        state.
        :return: bool
        """
        return _successLoginNotification or _profileButton

    def _parse_airdrops_table(self) -> ty.Iterable[ty.Tuple[str, str]]:
        """
        Parses table with the list of potential airdrops. Active window should
        be any of ongoing or participated airdrops
        # TODO: Add page validation
        # TODO: Add required table presence checks
        # TODO: Add found data validation too
        :return: An iterable of tuples containing airdrop name and its page url
        """
        links = self.driver.find_elements_by_css_selector("td a.cmc-link")
        for link in links:
            name = link.text
            href = link.get_attribute("href")
            relative = re.search(r"currencies.*", href).group(0)
            absolute_url = os.path.join(self.root_url, *relative.split("/"))

            yield name, absolute_url

    def _compose_airdrops(self) -> ty.List[Airdrop]:
        """
        Make airdrops from parsed table on current page
        :return:
        """
        if "airdrop" not in self.driver.current_url:
            raise ValueError("We are not on the airdrop page")

        airdrops = []
        for name, link in self._parse_airdrops_table():
            airdrop = Airdrop(
                name=name,
                url=link,
                telegram=self.telegram,
                twitter=self.twitter,
                addresses=self.addresses,
            )
            airdrops.append(airdrop)
        return airdrops

    def login(self) -> None:
        """
        Log in to coinmarketcap source with provided credentials.
        :return: None
        """
        if not self.logged_in:
            _loginButton.click()
            _loginModal.fill_and_submit(
                tag="type",
                fill_kw={
                    "email": self.credentials["email"],
                    "password": self.credentials["password"],
                },
            )
            if _successLoginNotification:
                self.logged_in = True

    @property
    def airdrops_url(self) -> str:
        """
        Compose ongoing airdrops page url from root url and predefined airdrops
        path
        :return: str - ongoing airdrops page link
        """
        return os.path.join(self.root_url, *"/airdrop/ongoing/".split("/"))

    @property
    def airdrops_participated_url(self):
        """
        Compose participated airdrops page url from root url and
        predefined airdrops path
        :return: str - participated airdrops page link
        """
        return os.path.join(
            self.root_url, *"/airdrop/participated/".split("/")
        )

    def get_ongoing_airdrops(self) -> ty.List[Airdrop]:
        """
        Loads page with ongoing airdrops. Compose Airdrop objects from all the
        found data from that page.
        :return: list of Airdrop objects
        """
        self.driver.get(self.airdrops_url)
        return self._compose_airdrops()

    def get_participated_airdrops(self) -> ty.List[Airdrop]:
        """
        Loads page with already participated airdrops. Compose Airdrop objects
        from all found data from that page.
        :return: list of Airdrop objects
        """
        self.driver.get(self.airdrops_participated_url)
        return self._compose_airdrops()

    def get_available_airdrops(self) -> ty.List[Airdrop]:
        """
        Takes all ongoing airdrops and returns only those that are not in
        participated list
        :return: list of Airdrop objects
        """
        participated = self.get_participated_airdrops()
        ongoing = self.get_ongoing_airdrops()
        return [o for o in ongoing if o not in participated]

    def process(self, config) -> None:
        """
        Airdrop source main entry point. Here all the stuff starts to execute.

        The first step is to load root page of current source. The link of it
        comes from configuration object.

        Then login to this website with provided credentials.
        The last step is to iterate through all found Airdrops and perform each

        :param config:
        :return:
        """
        self.root_page_load()
        self.login()

        available_airdrops = self.get_available_airdrops()
        for airdrop in available_airdrops:
            # try:
            airdrop.participate()
            # except Exception as e:
            # TODO: Add exceptions handle
            # print(traceback.format_exc())
            # print(str(e))
