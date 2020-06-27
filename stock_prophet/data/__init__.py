import data.db_connection as connector
import os

USERNAME = os.environ.get('USERNAME')
PASSWORD = os.environ.get('PASSWORD')
DB_NAME = os.environ.get('DB_NAME')
HOST = os.environ.get('HOST')
PORT = os.environ.get('PORT')


class Database:

    def __init__(self, username=USERNAME, password=PASSWORD, db_name=DB_NAME, host=HOST, port=PORT):
        self.engine, self.meta_data = connector.connect(username, password, db_name, host, port)

        if self.engine:
            self.stocks, self.analytics, self.markets, self.companies = connector.create_table(self.meta_data)
            self.meta_data.create_all(self.engine)

            print("Connect successful! You're awesome!")
        else:
            print("Connect is poo!")
