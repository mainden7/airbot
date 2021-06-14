import configparser
from airbot.providers.twitter import Twitter
from airbot.providers.telegram import Telegram


def start(args):
    cf = args.config_file
    config = configparser.ConfigParser()
    config.read(cf)

    for name, link in config["sources"].items():
        if name == "cmc":
            from airbot.sources.cmc.cmc import CMC

            with CMC(
                root_url=link,
                credentials=dict(
                    email=config[name]["login"],
                    password=config[name]["password"],
                ),
                twitter=Twitter(**config["twitter"]),
                telegram=Telegram(**config["telegram"]),
                addresses=dict(config["addresses"]),
            ) as source:
                source.process(config)
