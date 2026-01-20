import os
from dotenv import load_dotenv 

env_path = ".env"
load_dotenv(env_path)

SENDER_EMAIL = os.getenv("SENDER_EMAIL", "")
APP_PASSWORD = os.getenv("APP_PASSWORD", "")

if not SENDER_EMAIL:
    raise ValueError("SENDER_EMAIL environment variable is not set in .env file")
if not APP_PASSWORD:
    raise ValueError("APP_PASSWORD environment variable is not set in .env file")