#!/usr/bin/env python3
"""
Basic Flask app
"""

from flask import Flask, jsonify, make_response, abort
from flask import request, redirect, url_for
from auth import Auth


app = Flask(__name__)
AUTH = Auth()


@app.route("/")
def display_user():
    """
    returns json payload of the form
    {"message": "Bienvenue"}
    """
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"])
def register_user():
    """
    register user
    """
    try:
        email = request.form.get("email")
        password = request.form.get("password")

        if not email or not password:
            return jsonify({"message": "Email and password are required"}), 400

        """Attempt to register the user"""
        new_user = AUTH.register_user(email, password)
        return jsonify(
            {"email": new_user.email, "message": "user created"}), 200

    except ValueError as e:
        """User with email already exists"""
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'])
def login():
    """
    accept email and password from form data
    """
    email = request.form.get('email')
    password = request.form.get('password')
    if not AUTH.valid_login(email, password):
        abort(401)
    session_id = AUTH.create_session(email)
    resp = jsonify({"email": email, "message": "logged in"})
    resp.set_cookie("session_id", session_id)
    return resp


@app.route("/sessions", methods=["DELETE"], strict_slashes=False)
def logout() -> str:
    """destroye session using session_id"""
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if not user:
        abort(403)
    AUTH.destroy_session(user.id)
    return redirect(url_for("display_user"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
