import data.db_connection as connector

USERNAME = 'stonkboy'
PASSWORD = 'stonks228'
DB_NAME = 'stonks_db'
HOST = 'localhost'
PORT = '5432'


class Database:

    def __init__(self, username=USERNAME, password=PASSWORD, db_name=DB_NAME, host=HOST, port=PORT):
        con, meta_data = connector.connect(username, password, db_name, host, port)

        if con:
            self.stocks, self.analytics, self.markets, self.company = connector.create_table(meta_data)

            meta_data.create_all(con)
            print("Connect successful! You're awesome!")
        else:
            print("Connect is poo!")
