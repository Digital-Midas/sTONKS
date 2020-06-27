from data import Database

db1_name = 'stock'
db2_name = 'stock_prophet'


def row_to_market(row):
    return {
        'id': row[0],
        'name': row[1],
        'link_name': row[2]
    }


def row_to_company(row):
    return {
        'id': row[0],
        'name': row[1],
        'link_name': row[2],
        'code': row[3],
        'id_market': row[4]
    }


db1 = Database(db_name=db1_name)
db2 = Database(db_name=db2_name)

query = db1.markets.select()
markets = db1.engine.execute(query)
markets = list(map(row_to_market, markets))
db2.engine.execute(
    db2.markets.insert().values(
        markets
    )
)

query = db1.companies.select()
companies = db1.engine.execute(query)
companies = list(map(row_to_company, companies))
db2.engine.execute(
    db2.companies.insert().values(
        companies
    )
)