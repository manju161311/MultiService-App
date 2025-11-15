from flask import Flask, jsonify, request
import os
import requests
import time

app = Flask(__name__)

# Read auth service host from environment variables
AUTH_HOST = os.getenv("AUTH_HOST", "localhost")
AUTH_PORT = os.getenv("AUTH_PORT", "5100")
AUTH_URL = f"http://{AUTH_HOST}:{AUTH_PORT}"

@app.route("/health", methods=["GET"])
def health():
    return jsonify(service="api-gateway", status="ok", ts=time.time()), 200

@app.route("/login", methods=["POST"])
def login_proxy():
    data = request.get_json() or {}
    try:
        response = requests.post(
            AUTH_URL + "/login",
            json=data,
            timeout=2
        )
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify(error="auth-service unreachable", details=str(e)), 503

@app.route("/validate", methods=["POST"])
def validate_proxy():
    body = request.get_json() or {}
    token = body.get("token")

    if not token:
        return jsonify(valid=False, reason="token_missing"), 400

    try:
        response = requests.post(
            AUTH_URL + "/validate",
            json={"token": token},
            timeout=2
        )
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify(error="auth-service unreachable", details=str(e)), 503

@app.route("/hello", methods=["GET"])
def hello():
    return jsonify(message="hello from API Gateway"), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
