#!/usr/bin/env python3
""" Authentication
"""
from flask import Flask, jsonify, request, abort, redirect
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


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login() -> str:
    """ Login user """
    email = request.form.get('email')
    password = request.form.get('password')
    user = AUTH.valid_login(email, password)
    if not user:
        abort(401)
    id = AUTH.create_session(email)
    response = jsonify({"email": email, "message": "logged in"})
    response.set_cookie("session_id", id)
    return response


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout():
    """ logout """
    cookie = request.cookies.get("session_id", None)
    user = AUTH.get_user_from_session_id(cookie)
    if not cookie or not user:
        abort(403)
    AUTH.destroy_session(user.id)
    return redirect('/')


@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile() -> str:
    """ profile """
    cookie = request.cookies.get("session_id", None)
    if not cookie:
        abort(403)
    user = AUTH.get_user_from_session_id(cookie)
    if not user:
        abort(403)
    return jsonify({"email": user.email}), 200


@app.route('/reset_password', methods=['POST'], strict_slashes=False)
def get_reset_password_token() -> str:
    """ get reset password token """
    email = request.form.get('email')
    validate = AUTH.create_session(email)

    if not validate:
        abort(403)
    token = AUTH.get_reset_password_token(email)
    return jsonify(
        {"email": email, "reset_token": token}
    )


@app.route('/reset_password', methods=['PUT'], strict_slashes=False)
def update_password() -> str:
    """ update password """
    email = request.form.get('email')
    token = request.form.get('reset_token')
    new_pass = request.form.get('new_password')

    try:
        AUTH.update_password(token, new_pass)
    except Exception:
        abort(403)
    return jsonify(
        {"email": email, "message": "Password updated"}
    ), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
