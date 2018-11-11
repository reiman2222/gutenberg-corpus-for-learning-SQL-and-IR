import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey,REAL,CHAR
from sqlalchemy import inspect

'''
metadata = MetaData()
company = Table('company', metadata,
  Column('id', Integer, primary_key=True),
  Column('name', String),
  Column('age', Integer),
  Column('address', CHAR(50)),
  Column('salary', REAL)
)
'''

POSTGRES = {
    'user': 'postgres',
    'pw': 'postgres',
    'db': 'gutenburg',
    'host': 'localhost',
    'port': '5432',
    }
#engine = create_engine('postgresql://postgres:password@localhost:5432/my_database')
'''engine = create_engine('postgresql://postgres:password@localhost:5432/my_database')

with engine.connect() as con:

    rs = con.execute('SELECT * FROM company')
    for row in rs:
        id,name,age,address,salary = rs
        print(row)
'''