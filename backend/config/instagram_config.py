import os
from dotenv import load_dotenv

load_dotenv()

class InstagramAPIConfig:
    BASE_URL = "https://instagram-scraper-api2.p.rapidapi.com"
    RAPIDAPI_HOST = "instagram-scraper-api2.p.rapidapi.com"
    RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY") # Assuming RAPIDAPI_KEY is in .env

    def __init__(self):
        if not self.RAPIDAPI_KEY:
            raise ValueError("RAPIDAPI_KEY environment variable not set.")
