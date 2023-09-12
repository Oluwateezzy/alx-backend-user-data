#!/usr/bin/env python3
""" Module of session views
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User
from api.v1.app import auth
from os import getenv


@app_views.route(
    '/auth_session/login', methods=['POST'], strict_slashes=False
)
def login() -> str:
    """ login user"""
    email = request.form.get("email")
    password = request.form.get("password")

    if not email:
        return jsonify({"error": "email missing"}), 400
    if not password:
        return jsonify({"error": "password missing"}), 400
    user = User.search({"email": email})
    if not user:
        return jsonify({"error": "no user found for this email"}), 404
    if not user[0].is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401
    session_cookie = getenv("SESSION_NAME")
    session = auth.create_session(user[0].to_json()["id"])
    res = jsonify(user[0].to_json())
    res.set_cookie(session_cookie, session)
    return res


@app_views.route(
    'auth_session/logout', methods=['DELETE'], strict_slashes=False
)
def logout():
    """ Logout user """
    destroy = auth.destroy_session(request)
    if not destroy:
        return False, abort(404)
    return jsonify({}), 200
