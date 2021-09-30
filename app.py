from sqlalchemy import create_engine, select, MetaData
from sqlalchemy.dialects.sqlite import insert
from sqlalchemy.orm import Session

from db import Database, commands
from models import metadata, table


class InputError(Exception):
    def __init__(self, message):
        # Call the base class constructor with the parameters it needs
        super().__init__(message)


def take_input():
    try:
        args = str(input()).split(' ')
        args_count = len(args)

        # if args_count == 0:
        #     raise InputError('no args')

        if args_count > 0 and args[0] not in commands:
            raise InputError(f'unknown command: {args[0]}')

    except EOFError:
        print('EOF when reading a line. Stop working...')
        return 'EOF'
    except InputError:
        return None
    else:
        return tuple(args)


def db_loop():

    db = Database()
    result = None
    while result != 'EOF':
        console_args = take_input()
        result = db.execute(console_args)
        print(result)

    """
    db schema:
    id  |   varname     |   value
    0   |   A           |   1
    1   |   B           |   3

    create db object, with engine, session, metadata

    read console -> check if command in cmd_set: verify_command(cmd_str: str) return (*args)

    cmd_name, *args = args, use db.commands[cmd_name](args)

    """


if __name__ == '__main__':
    db_loop()
