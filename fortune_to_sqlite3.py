#!/usr/bin/env python

import getopt, sys
import sqlite3

def usage():
    pass

def parse_args(args):
    pass

def read_fortunes(fortunes_path):
    with open(fortunes_path) as f:
        [fortune for fortune in f.read().split("\n%\n") if len(fortune) > 0]

def create_schema_if_needed(db):
    db.execute('CREATE TABLE IF NOT EXISTS fortunes (body text)')
    db.commit()

def add_fortunes(db, fortunes):
    db.executemany('INSERT INTO fortunes VALUES (?)', fortunes)
    db.commit()

if __name__ == "__main__":
    try:
        (help_needed, fortunes_path, database_path) = parse_args(sys.argv[1:])
    except getopt.GetoptError as err:
        print str(err)
        usage()
        sys.exit(2)
    

    if help_needed:
        usage()
        sys.exet(0)

    with sqlite3.connect(database_path) as db:
        create_schema_if_needed(db)
        fortunes = [(fortune,) for fortune in read_fortunes(fortunes_path)]
        add_fortunes(db, fortubes)
