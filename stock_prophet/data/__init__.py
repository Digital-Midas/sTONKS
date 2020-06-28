import data.db_connection as connector
import os
from dotenv import load_dotenv

dotenv_path = os.path.join('./../.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
else:
    print('Can`t find .env file.')

USERNAME = os.environ.get('DB_USERNAME')
PASSWORD = os.environ.get('DB_PASSWORD')
DB_NAME = os.environ.get('DB_NAME')
HOST = os.environ.get('DB_HOST')
PORT = os.environ.get('DB_PORT')


class Database:

    def __init__(self, username=USERNAME, password=PASSWORD, db_name=DB_NAME, host=HOST, port=PORT):
        self.engine, self.meta_data = connector.connect(username, password, db_name, host, port)

        if self.engine:
            self.stocks, self.analytics, self.markets, self.companies = connector.create_table(self.meta_data)
            self.meta_data.create_all(self.engine)

            print("Connect successful! You're awesome!")
        else:
            print("Connect is poo!")
