commands = {
    'SET',      # SET A 1
    'GET',      # GET A     -> 1
    'UNSET',    # UNSET A
    'COUNTS',   # COUNTS 1  -> 2
    'FIND',     # FIND 1    -> A, B
    'END',
    'BEGIN',
    'ROLLBACK',
    'COMMIT',
}


class Database:
    def __init__(self):
        self.engine = create_engine("sqlite+pysqlite:///:memory:", echo=True, future=True)
        MetaData().create_all(self.engine)
        # self.metadata.create_all(engine)
        self.session = Session(self.engine)

        print('Create :memory: database...\nDone!\n\nPlease, input transaction:')

    def execute(self, cmd, *args, **kwargs):
        try:
            result = commands[cmd](*args, **kwargs)
        except IndexError:
            print('Неверное количество аргументов')
        except ValueError:
            print('Ошибка ввода значения переменной')
        except EOFError:
            raise EOFError
        else:
            return result

    def set(self, *args):
        name = args[0]
        value = int(args[1])
        if len(args) > 2:
            raise IndexError

    def get(self, *args):
        name = args[0]
        if len(args) > 1:
            raise IndexError

        result = session.get()
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


