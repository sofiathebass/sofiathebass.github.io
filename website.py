from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/")
def index():
    return "hacc"

@app.route("/upload", methods=["POST"])
def upload():
    if request.method == "POST":
        play_script = str(request.json["play"])
        return jsonify("Received")

if __name__ == "__main__":
    app.run()