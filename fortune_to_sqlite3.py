#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from sqlalchemy import create_engine
from fortune import schema

def usage():
    print 'fortune_to_sqlite3.py <fortune-path> <database-path>'

def parse_args(args):
    fortune_path = None
    database_path = None

    if len(args) >= 2:
        fortune_path = args[0]
        database_path = args[1]

    help_needed = fortune_path == None or database_path == None

    return help_needed, fortune_path, database_path

def read_fortunes(fortunes_path):
    with open(fortunes_path) as f:
        return [fortune.decode('utf-8')
                for fortune in f.read().split("\n%\n")
                if len(fortune) > 0]

def add_fortunes(db, fortunes):
    db.execute(schema.fortunes.insert(),
               [{'body': fortune} for fortune in fortunes])

def main():
    help_needed, fortunes_path, database_path = parse_args(sys.argv[1:])

    if help_needed:
        usage()
        sys.exit(0)

    engine = create_engine('sqlite:///' + database_path)

    schema.metadata.create_all(engine)

    with engine.connect() as db:
        add_fortunes(db, read_fortunes(fortunes_path))

if __name__ == '__main__':
    main()
