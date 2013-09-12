#!/usr/bin/env python

import sys
import sqlite3

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
        return [fortune
                for fortune in f.read().split("\n%\n")
                if len(fortune) > 0]

def create_schema_if_needed(db):
    db.execute('create table if not exists fortunes ('
               'id integer not null primary key autoincrement,'
               'body text'
               ')')
    db.commit()

def add_fortunes(db, fortunes):
    db.executemany('insert into fortunes (body) values (?)',
                   [(fortune,) for fortune in fortunes])
    db.commit()

def main():
    help_needed, fortunes_path, database_path = parse_args(sys.argv[1:])

    if help_needed:
        usage()
        sys.exit(0)

    with sqlite3.connect(database_path) as db:
        db.text_factory = str
        create_schema_if_needed(db)
        add_fortunes(db, read_fortunes(fortunes_path))

if __name__ == '__main__':
    main()
