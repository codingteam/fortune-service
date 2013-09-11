#!/usr/bin/env python

from flask import Flask, Response
import sqlite3
import json

app = Flask(__name__)

def get_random_fortune(db):
    for row in db.execute('select * from fortunes order by random() limit 1'):
        return row[0]

@app.route('/api/random')
def fortune():
    with sqlite3.connect('./fortunes.db') as db:
        return Response(json.dumps({'body': get_random_fortune(db)},
                                   sort_keys=True,
                                   indent=4,
                                   separators=(',', ': ')),
                        mimetype='application/json')

if __name__ == '__main__':
    app.debug = True
    app.run();
