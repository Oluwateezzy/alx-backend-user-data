#!/usr/bin/env python3
""" Authentication
"""
from flask import Flask, jsonify, request
from sqlalchemy.orm.exc import NoResultFound
from auth import Auth


app = Flask(__name__)
AUTH = Auth()

@app.route('/', methods=['GET'], strict_slashes=False)
def index():
    """ index """
    return jsonify({"message": "Bienvenue"})

@app.route('/users', methods=['POST'], strict_slashes=False)
def create() -> str:
    """ create user """
    email = request.form.get('email')
    password = request.form.get('password')
    
    try:
        user = AUTH.register_user(email, password)
        if user:
            return jsonify({
                "email": user.email,
                "message": "user created"
            })
    except ValueError:
        return jsonify({
            "message": "email already registered"
        }), 400
        

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")