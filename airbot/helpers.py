import requests


def open_url(link):
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) "
            "Gecko/20100101 Firefox/45.0"
        )
    }
    return requests.get(link, headers=headers)
