import re
from airbot.logger import log
from telethon.sync import TelegramClient
from telethon.tl.functions.channels import JoinChannelRequest


class Telegram:
    """
    General interface to process all telegram related tasks.
    Authorizes though CLI in the first time call.

    Args:
        :param name: str - Telegram profile login
        :param api_id: - Telegram api ID. Register your app in
        telegram developer page to get this value
        :param api_hash: same as app id
    """

    def __init__(self, name: str, api_id: int, api_hash: str):
        self.name = name
        self.api_id = api_id
        self.api_hash = api_hash

    def join_group(self, link: str) -> None:
        """
        Joins provided channel. Entity is created from link. Looks like
        https://t.me/channel_name

        Parses last 10 messages and checks whether they addressed to our user
        with some puzzle that need to be solved to avoid kick from that chat.

        Currently supported only math puzzle

        :param link: telegram channel link
        :return: None

        TODO: Add support of more channel bot tasks such as communication with
        bot and others
        """
        with TelegramClient("anon", self.api_id, self.api_hash) as client:
            channel = client.get_entity(link)
            client(JoinChannelRequest(channel))
            for idx, message in enumerate(client.iter_messages(channel)):
                if "@asynchandler" in message.text:
                    log.info(f"Message found: {message.text}")
                    if "arithmetic" in message.text:
                        expr = re.findall(r"(?<=\().*?(?=\))", message.text)
                        if expr:
                            math_expr = expr[0]
                            if re.match(
                                r"(\d+)\s.+|-|\^|/|\*(\d+)", math_expr
                            ):
                                answer = eval(math_expr)
                                client.send_message(
                                    entity=channel, message=str(answer)
                                )
                                log.info(
                                    f"Solve math expression: {math_expr},"
                                    f" {answer=}. Message sent"
                                )

                    elif "click" in message.text.lower():
                        # FIXME: buttons from bots are not clickable somehow
                        message.click()

                    break

                if idx == 10:
                    break
