#!/usr/bin/env python

from flask import Flask, Response
from sqlalchemy import create_engine
from sqlalchemy.sql import select, and_
from sqlalchemy.sql.functions import char_length, random
from fortune_schema import fortunes
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

engine = create_engine('sqlite:///' + app.config['DATABASE'])

def get_random_fortune(db):
    s = select(
        [fortunes.c.id, fortunes.c.body]
    ).where(
        char_length(fortunes.c.body) <= 128
    ).order_by(
        random()
    ).limit(1)

    return db.execute(s).fetchone()

def get_fortune_body_by_id(db, fortune_id):
    s = select(
        [fortunes.c.body]
    ).where(
        and_(
            fortunes.c.id == fortune_id,
            char_length(fortunes.c.body) <= 128
        )
    )

    result = db.execute(s).fetchone()

    if result != None:
        return result[0]
    else:
        return None

def dict_as_response(dictionary):
    return Response(json.dumps(dictionary, indent=4, separators=(',', ': ')),
                    mimetype='application/json')

def fortune_response(fortune_id, fortune_body):
    return dict_as_response({'id': fortune_id,
                             'body': fortune_body,
                             'status': 'ok'})

def not_found_response():
    return dict_as_response({'status': 'not_found'})

@app.route('/api/random')
def route_api_random():
    with engine.connect() as db:
        random_fortune = get_random_fortune(db)
        if random_fortune != None:
            (fortune_id, fortune_body) = random_fortune
            return fortune_response(fortune_id, fortune_body)
        else:
            return not_found_response()

@app.route('/api/<int:fortune_id>')
def route_api_fortune_by_id(fortune_id):
    if fortune_id >= 2 ** 63:
        return not_found_response()

    with engine.connect() as db:
        fortune_body = get_fortune_body_by_id(db, fortune_id)
        if fortune_body != None:
            return fortune_response(fortune_id, fortune_body)
        else:
            return not_found_response()

if __name__ == '__main__':
    app.run()
