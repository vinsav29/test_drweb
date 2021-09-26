from sqlalchemy import create_engine, select
from sqlalchemy.dialects.sqlite import insert
from sqlalchemy.orm import Session
from models import metadata, table

_3arg_commands = {
    'SET',  # SET A 10
}

_2arg_commands = {
    'GET',  # GET A
    'UNSET',  # UNSET A
    'COUNTS',  # COUNTS 10
}

_1arg_commands = {
    'FIND',
    'END',
    'BEGIN',
    'ROLLBACK',
    'COMMIT',
}


class InputError(Exception):
    def __init__(self, message):
        # Call the base class constructor with the parameters it needs
        super().__init__(message)


def take_input():
    try:
        args = str(input()).split(' ')
        args_count = len(args)

        if args_count == 0:
            raise InputError('no args')

        if args_count > 0:
            if args[0] not in _1arg_commands | _2arg_commands | _3arg_commands:
                raise InputError(f'unknown command: {args[0]}')

        if args_count == 1 and args[0] not in _1arg_commands or \
                args_count == 2 and args[0] not in _2arg_commands or \
                args_count == 3 and args[0] not in _3arg_commands:
            raise InputError(f'wrong number of arguments with command: {args[0]}')

        if args_count > 1:
            check_num = '1'
            check_str = 'B'
            if args[0] == 'COUNTS':
                check_num = args[1]
            elif args[0] == 'SET':
                check_str = args[1]
                check_num = args[2]
            else:
                check_str = args[1]
            if not check_str.isalpha():
                raise InputError(f'varname {check_str} must be a string')
            if not check_num.isnumeric():
                raise InputError(f'{check_num} must be a number')

    except EOFError:
        print('EOF when reading a line. Stop working...')
        raise EOFError
    except Exception as e:
        print(e)
    else:
        return ' '.join(args)


def db_loop():
    while True:
        try:
            take_input()
        except EOFError:
            return
        except Exception as e:
            print(e)
        else:
            pass
        finally:
            pass


if __name__ == '__main__':
    engine = create_engine('sqlite://')
    metadata.create_all(engine)
    session = Session(engine)

    print('Create :memory: database...\nDone!\n\nPlease, input transaction:')

    # SET
    # https://docs.sqlalchemy.org/en/14/dialects/sqlite.html?highlight=upsert#sqlite-on-conflict-insert
    insert_stmt = insert(table).values(varname='A', value=1)
    update_stmt = insert_stmt.on_conflict_do_update(index_elements=['varname'], set_={'value': 1})
    session.execute(update_stmt)

    # BEGIN
    savepoint = session.begin_nested()

    insert_stmt = insert(table).values(varname='A', value=2)
    update_stmt = insert_stmt.on_conflict_do_update(index_elements=['varname'], set_={'value': 2})
    session.execute(update_stmt)

    # ROLLBACK
    savepoint.rollback()

    insert_stmt = insert(table).values(varname='B', value=1)
    update_stmt = insert_stmt.on_conflict_do_update(index_elements=['varname'], set_={'value': 1})
    session.execute(update_stmt)

    # GET
    statement = select(table).filter_by(varname="A")
    result = session.execute(statement).all()
    print(result)

    # FIND
    from sqlalchemy import column
    from sqlalchemy import values
    statement = select(table).filter_by(value=1)
    result = session.execute(statement).all()
    print(result)

    # COUNTS
    # https: // stackoverflow.com / questions / 12941416 / how - to - count - rows - with-select - count -with-sqlalchemy
    from sqlalchemy import func
    statement = select([func.count()]).select_from(table).filter_by(value=1)
    result = session.execute(statement).all()
    print(result)

    # db_loop()
    """
    db schema:
    id  |   varname     |   value
    0   |   A           |   1
    1   |   B           |   3
    
    read console to cmd_str
    check if command in cmd_set: verify_command(cmd_str: str) -> (*args)
     
    """
