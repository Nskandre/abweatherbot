import os
from dotenv import load_dotenv

load_dotenv()

OPEN_WEATHER_TOKEN = os.getenv("OPEN_WEATHER_TOKEN", '')
TG_TOKEN = os.getenv("TG_TOKEN", '')
