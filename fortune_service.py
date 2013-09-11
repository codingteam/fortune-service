#!/usr/bin/env python

from flask import Flask, Response
import sqlite3
import json

app = Flask(__name__)

def get_random_fortune(db):
    for row in db.execute('select id, body from fortunes '
                          'order by random() limit 1'):
        return row

@app.route('/api/random')
def fortune():
    with sqlite3.connect('./fortunes.db') as db:
        (fortune_id, fortune_body) = get_random_fortune(db)
        return Response(json.dumps({'id': fortune_id,
                                    'body': fortune_body},
                                   indent=4,
                                   separators=(',', ': ')),
                        mimetype='application/json')

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0');
