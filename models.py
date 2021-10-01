from sqlalchemy import Table, Column, Integer, String, MetaData
from sqlalchemy.orm import declarative_base
# metadata = MetaData()
Base = declarative_base()


class Var(Base):
    __tablename__ = 'variable'

    name = Column(String, primary_key=True)
    value = Column(Integer)

    def __repr__(self):
        return f"Var(name={self.name!r}, value={self.value!r})"


# table = Table(
#     'table', metadata,
#     Column('name', String, primary_key=True),
#     Column('value', Integer, nullable=False)
# )

