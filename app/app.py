from flask import Flask, request, jsonify, render_template
# from flask_cors import CORS

app = Flask(__name__)
# CORS(app)

@app.route("/")
def index():
    """
    The homepage for our beautiful stunning website.
    """
    return render_template("app/home.html")

@app.route("/speak")
def speak():
    """
    The page for the user to input their voice.
    """
    return render_template("app/speak.html")

@app.route("/upload", methods=["POST"])
def upload():
    """
    The upload page for our beautiful stunning website with a upload button
    for the chosen play.
    """
    if request.method == "POST":
        play_script = str(request.json["play"])
        return jsonify("Received")

if __name__ == "__main__":
    app.run()