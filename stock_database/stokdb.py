import sqlalchemy
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Date, ForeignKey, Float
import psycopg2


def connect(user, password, database, host='localhost', port='5432'):
    # postgresql://user:password@host:port/database
    url = 'postgresql+psycopg2://{}:{}@{}:{}/{}'
    url = url.format(user, password, host, port, database)

    try:
        con = create_engine(url, client_encoding='utf8')
        meta_data = MetaData(bind=con, reflect=True)
    except sqlalchemy.exc.OperationalError:
        print("Database doesn't exists or username/password incorrect.")
        return False, False
    else:
        return con, meta_data


def create_table(meta_data):
    try:
        stoks = Table(
            'stoks', meta_data,
            Column('id_company', Integer, primary_key=True),
            Column('date', Date, primary_key=True),
            Column('high', Float),
            Column('low', Float),
            Column('open', Float),
            Column('close', Float),
            Column('vol', Float)

        )   

        analytics = Table(
            'analytics', meta_data,
            Column('id_anal', Integer, ForeignKey('stoks.id_company')),
            Column('name', String),
            Column('rating', Float)
        )

        markets = Table(
            'markets', meta_data,
            Column('id_market', Integer, primary_key=True),
            Column('name', String),
            Column('linkname', String)
        )

        company = Table(
            'company', meta_data,
            Column('id_compamy', Integer, ForeignKey('stoks.id_company')),
            Column('name', String),
            Column('linkname', String),
            Column('id_market', Integer, ForeignKey('markets.id_market'))
        )
    except sqlalchemy.exc.InvalidRequestError:
        print("All table is already.")
        return meta_data.tables['stoks'], meta_data.tables['analytics'], \
            meta_data.tables['markets'], meta_data.tables['company']
    else:
        return stoks, analytics, markets, company


con, meta_data = connect('stonkboy', 'stonks228', 'stonks_db')

if con != False: 
    stoks, analytics, markets, company =  create_table(meta_data)

    meta_data.create_all(con)
    print("Connect successful! You're awesome!")       
else:
    print("Connect is poo!")





