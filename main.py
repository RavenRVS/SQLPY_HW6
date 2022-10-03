import json

import sqlalchemy
from sqlalchemy.orm import sessionmaker

from models import create_tables, Publisher, Book, Stock, Sale, Shop

base_type = 'postgresql'
user_name = 'postgres'
pwd = 'ravenrvs'
host = 'localhost'
port = '5432'
base_name = 'book_shop_db'

DSN = f"{base_type}://{user_name}:{pwd}@{host}:{port}/{base_name}"
engine = sqlalchemy.create_engine(DSN)
create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()

with open('fixtures/tests_data.json', encoding='utf-8') as f:
    data = json.load(f)
    for d in data:
        if d['model'] == 'publisher':
            str = Publisher(id=d['pk'], name=d['fields']['name'])
            session.add(str)
            session.commit()
        if d['model'] == 'book':
            str = Book(id=d['pk'], title=d['fields']['title'], id_publisher=d['fields']['id_publisher'])
            session.add(str)
            session.commit()
        if d['model'] == 'shop':
            str = Shop(id=d['pk'], name=d['fields']['name'])
            session.add(str)
            session.commit()
        if d['model'] == 'stock':
            str = Stock(id=d['pk'], id_shop=d['fields']['id_shop'], id_book=d['fields']['id_book'],
                        count=d['fields']['count'])
            session.add(str)
            session.commit()
        if d['model'] == 'sale':
            str = Sale(id=d['pk'], price=d['fields']['price'], date_sale=d['fields']['date_sale'],
                       count=d['fields']['count'], id_stock=d['fields']['id_stock'])
            session.add(str)
            session.commit()

x_publisher = int(input('Enter publisher id: '))

q_pub = session.query(Publisher).filter(Publisher.id == x_publisher)
subq = session.query(Book).filter(Book.id_publisher == x_publisher).subquery()
subq2 = session.query(Stock).join(subq, Stock.id_book == subq.c.id).subquery()
q = session.query(Shop).join(subq2, Shop.id == subq2.c.id_shop)
for p in q_pub:
    print(f'Publisher {p.name} there is:')
for s in q.all():
    print(s.name)
