import logging
import os

from dotenv import load_dotenv

# Set up the environment from `.env`
load_dotenv()
if "DISCORD_BOT_TOKEN" not in os.environ:
    raise RuntimeError("DISCORD_BOT_TOKEN must be defined in the environment.")