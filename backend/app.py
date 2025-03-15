# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
from auth import register_user, login_user
from chat import chat_with_model
from db import init_db, db

app = Flask(__name__)
CORS(app)
init_db(app)

with app.app_context():
    db.create_all()

@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    return register_user(data)

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    return login_user(data)

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    return chat_with_model(data)

if __name__ == '__main__':
    app.run(debug=True)