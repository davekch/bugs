import os
from configparser import ConfigParser
from django.core.management import utils
from .common import *

SERVER_CONFIG_PATH = os.path.join(BASE_DIR, "bugtrack", "settings", "productionsettings.ini")

config = ConfigParser(interpolation=None)
if not os.path.isfile(SERVER_CONFIG_PATH):
    config["server"] = {
        "allowed": "127.0.0.1",
        "secret": utils.get_random_secret_key(),
    }
    with open(SERVER_CONFIG_PATH, "w") as f:
        config.write(f)
else:
    config.read(SERVER_CONFIG_PATH)

DEBUG = False

ALLOWED_HOSTS = config["server"]["allowed"].split(",")

SECRET_KEY = config["server"]["secret"]
