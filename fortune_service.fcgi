#!/usr/bin/env python

from flup.server.fcgi import WSGIServer
from fortune_service import app

if __name__ == '__main__':
    WSGIServer(app, bindAddress='/tmp/fcgi.sock').run()
