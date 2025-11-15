from flask import Flask, jsonify, request, abort
import os
import time
import jwt

app = Flask(__name__)
JWT_SECRET = os.getenv("JWT_SECRET", "devsecret")
JWT_ALG = "HS256"

# Dummy users
USERS = {
    "alice": "password1",
    "bob": "password2"
}

@app.route("/health", methods=["GET"])
def health():
    return jsonify(service="auth-service", status="ok", ts=time.time()), 200

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json() or {}
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify(error="username and password required"), 400
    
    if username not in USERS or USERS[username] != password:
        return jsonify(error="invalid credentials"), 401
    
    payload = {"sub": username, "iat": int(time.time())}
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALG)

    return jsonify(access_token=token, token_type="bearer"), 200

@app.route("/validate", methods=["POST"])
def validate():
    data = request.get_json() or {}
    token = data.get("token")

    if not token:
        return jsonify(valid=False, reason="missing token"), 400
    
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALG])
        return jsonify(valid=True, subject=payload.get("sub")), 200
    except jwt.ExpiredSignatureError:
        return jsonify(valid=False, reason="expired"), 401
    except Exception as e:
        return jsonify(valid=False, reason=str(e)), 401

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
