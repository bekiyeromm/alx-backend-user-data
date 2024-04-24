#!/usr/bin/env python3
"""
Basic Flask app
"""

from flask import Flask, jsonify
from flask import request
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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
