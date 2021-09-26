from sqlalchemy import Table, Column, Integer, String, MetaData
metadata = MetaData()

table = Table(
    'table', metadata,
    Column('varname', String, primary_key=True),
    Column('value', Integer, nullable=False)
)