from data import Database
from web import browser
import os
from dotenv import load_dotenv

db = Database()
browser.fill_all_markets_and_companies(db)
