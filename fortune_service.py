#!/usr/bin/env python

from flask import Flask, Response
import sqlite3
import json

app = Flask(__name__)
app.config.from_envvar('FORTUNE_SERVICE_CONFIG')
if app.debug is not True:
    import logging
    from logging.handlers import RotatingFileHandler

    file_handler = RotatingFileHandler('/tmp/fortune_service.log',
                                       maxBytes = 10 * 1024 * 1024,
                                       backupCount = 20)
    file_handler.setLevel(logging.ERROR)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)
    app.logger.addHandler(file_handler)

def get_random_fortune(db):
    for row in db.execute('select id, body from fortunes '
                          'order by random() limit 1'):
        return row

def fortune_response(fortune_id, fortune_body):
    return Response(json.dumps({'id': fortune_id,
                                'body': fortune_body},
                               indent=4,
                               separators=(',', ': ')),
                    mimetype='application/json')

@app.errorhandler(500)
def internal_error(exception):
    app.logger.exception(exception)
    return render_template('500.html'), 500

@app.route('/api/random')
def route_api_random():
    with sqlite3.connect(app.config['DATABASE']) as db:
        (fortune_id, fortune_body) = get_random_fortune(db)
        return fortune_response(fortune_id, fortune_body)

if __name__ == '__main__':
    app.run()
