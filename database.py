from sqlalchemy import create_engine, select, MetaData
from sqlalchemy.dialects.sqlite import insert
from sqlalchemy.orm import Session
from models import Var, Base


class Database:
    commands = dict()
    session = None

    def __init__(self):
        self.engine = create_engine("sqlite+pysqlite:///:memory:", echo=True, future=True)
        # MetaData().create_all(self.engine)
        # self.metadata.create_all(engine)
        Base.metadata.create_all(self.engine)
        self.session = Session(self.engine)

        self.commands = {
            'SET': self.set,  # SET A 1
            'GET': self.get,  # GET A     -> 1
            'UNSET': self.unset,  # UNSET A
            'COUNTS': self.counts,  # COUNTS 1  -> 2
            'FIND': self.find,  # FIND 1    -> A, B
            'END': self.end,
            'BEGIN': self.begin,
            'ROLLBACK': self.rollback,
            'COMMIT': self.commit,
        }

        print('Create :memory: database...\nDone!\n\nPlease, input transaction:')

    def execute(self, cmd, *args, **kwargs):
        try:
            return self.commands[cmd](*args, **kwargs)
        except IndexError:
            print('Неверное количество аргументов')
        except ValueError:
            print('Ошибка ввода значения переменной')
        except EOFError:
            raise EOFError
        except KeyError:
            print('Неизвестная команда')
        return None

    def set(self, *args):
        name = str(args[0])
        value = int(args[1])
        print(name, value)
        if len(args) > 2:
            raise IndexError
        # insert_stmt = insert(table).values(varname='A', value=1)
        # update_stmt = insert_stmt.on_conflict_do_update(index_elements=['varname'], set_={'value': 1})
        # result = self.session.execute(update_stmt)
        result = self.session.add(Var(name=name, value=value))
        return None

    def get(self, *args):
        name = args[0]
        if len(args) > 1:
            raise IndexError

        result = self.session.query(Var).filter_by(name=name).scalar()
        if result:
            return result
        else:
            return 'NULL'

    def unset(self, *args):
        name = args[0]

    def counts(self, *args):
        value = int(args[0])
        if len(args) > 1:
            raise IndexError

    def find(self, *args):
        value = int(args[0])
        if len(args) > 1:
            raise IndexError

    def end(self, *args):
        # db in memory, no need to commit changes
        if args:
            raise IndexError
        self.session.close()
        raise EOFError

    def begin(self, *args):
        pass

    def rollback(self, *args):
        pass

    def commit(self, *args):
        pass

# from sqlalchemy import create_engine, text
# engine = create_engine("sqlite+pysqlite:///:memory:", echo=True, future=True)
#
# from sqlalchemy.orm import declarative_base
# Base = declarative_base()
#
# from sqlalchemy import Table, Column, Integer, String
# class Var(Base):
#     __tablename__ = 'variable'
#
#     name = Column(String, primary_key=True)
#     value = Column(Integer)
#
#     def __repr__(self):
#         return f"Var(name={self.name!r}, value={self.value!r})"
#
#
# from sqlalchemy.orm import Session
# with Session(engine) as session:
#     session.execute(text("CREATE TABLE some_table (x int, y int)"))
#     session.execute(text("INSERT INTO some_table (x, y) VALUES (:x, :y)"), [{"x": 1, "y": 1}, {"x": 2, "y": 4}])
#     session.execute(text("INSERT INTO some_table (x, y) VALUES (:x, :y)").bindparams(x=3, y=8))
#
#     session.execute(text("CREATE TABLE some_table (x int, y int)"))
#
#     # session.commit()
#
#     result = session.execute(text("SELECT x, y FROM some_table"))
#     for row in result:
#         print(f"x: {row.x}  y: {row.y}")
