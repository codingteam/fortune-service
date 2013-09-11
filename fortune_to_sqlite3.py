#!/usr/bin/env python

import getopt, sys
import sqlite3

def usage():
    print 'fortune_to_sqlite3.py [-h] [-f <fortune-path>] [-d <database-path>]'

def parse_args(args):
    opts, _ = getopt.getopt(args, "hf:d:", ["help", "fortune", "database"])
    help_needed = False
    fortune_path = None
    database_path = None

    for o, a in opts:
        if o in ("-h", "--help"):
            help_needed = True
        elif o in ("-f", "--fortune"):
            fortune_path = a
        elif o in ("-d", "--database"):
            database_path = a
        else:
            assert False, "unhandled option"

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
    try:
        help_needed, fortunes_path, database_path = parse_args(sys.argv[1:])
    except getopt.GetoptError as err:
        print str(err)
        usage()
        sys.exit(2)

    if help_needed:
        usage()
        sys.exit(0)

    with sqlite3.connect(database_path) as db:
        db.text_factory = str
        create_schema_if_needed(db)
        add_fortunes(db, read_fortunes(fortunes_path))

if __name__ == "__main__":
    main()
