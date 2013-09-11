#!/usr/bin/env python

from flask import Flask, Response

app = Flask(__name__)

@app.route("/fortune")
def fortune():
    return "Not implemented yet!"

if __name__ == "__main__":
    app.run();
