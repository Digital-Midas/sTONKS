from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Date, ForeignKey, REAL


def connect(user, password, database, host='localhost', port='5432'):
    # postgresql://user:password@host:port/database
    url = 'postgresql+psycopg2://{}:{}@{}:{}/{}'
    url = url.format(user, password, host, port, database)

    con = create_engine(url, client_encoding='utf8')
    meta_data = MetaData(bind=con, reflect=True)

    return con, meta_data


con, meta_data = connect('stonkboy', 'stonks228', 'stonks_db')

stoks = Table(
    'stoks', meta_data,
    Column('id_org', Integer, primary_key=True),
    Column('org_name', String),
    Column('date', Date),
    Column('stock_price', REAL)
)
analytics = Table(
    'analytics', meta_data,
    Column('id', Integer, ForeignKey('stoks.id_org')),
    Column('name', String),
    Column('rating', REAL)
)

meta_data.create_all(con)


