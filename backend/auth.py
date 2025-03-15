# auth.py
from models.user import User
from db import db
from flask import jsonify


def register_user(data):
    username = data.get('username')
    password = data.get('password')
    if User.query.filter_by(username=username).first():
        return jsonify({"error": "User already exists"}), 400
    new_user = User(username=username, password=password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User registered successfully"})

def login_user(data):
    username = data.get('username')
    password = data.get('password')
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        return jsonify({"message": "Login successful"})
    return jsonify({"error": "Invalid credentials"}), 401