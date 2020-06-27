from data import Database
from web import browser
import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
else:
    print('Can`t find .env file.')

db = Database()
browser.fill_all_markets_and_companies(db)
