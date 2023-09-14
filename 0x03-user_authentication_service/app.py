#!/usr/bin/env python3
""" Authentication
"""
from flask import Flask, jsonify


app = Flask(__name__)

app.route('/')
def index():
    """ index """
    return jsonify({}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")