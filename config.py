from dotenv import load_dotenv

import os
from os.path import (
    join,
    dirname,
    abspath,
    splitext
)

"""PATHS"""
ROOT = abspath(dirname(__file__))
RESOURCES = join(ROOT, "resources")

STARRAIL  = join(RESOURCES, "starrail")
SFONTS = join(STARRAIL, "fonts")

CONFIG = join(ROOT, "config", ".env")

COG_FOLDER = join(ROOT, "cogs")

"""BOT"""
load_dotenv(CONFIG, encoding="utf-16")

TOKEN = os.environ["token"]
COGS = ["cogs.%s" % splitext(cog)[0] for cog in os.listdir(COG_FOLDER) if splitext(cog)[1] == ".py"]

spotify_green = 0x1DB954
spotify_black = 0x191414

"""SPOTIFY"""
spotify_client = os.environ["client_id"]
spotify_secret = os.environ["client_secret"]

