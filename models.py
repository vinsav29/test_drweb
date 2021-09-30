from sqlalchemy import Table, Column, Integer, String, MetaData
metadata = MetaData()


# class Var(Model):
#     name = Column

table = Table(
    'table', metadata,
    Column('name', String, primary_key=True),
    Column('value', Integer, nullable=False)
)

