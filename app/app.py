from flask import Flask, request, jsonify, render_template, redirect, url_for
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
    script = request.args.get('script')
    return render_template("app/speak.html", script=script)

@app.route("/uploadLine", methods=["POST"])
def uploadLine():
    """
    The upload page for our beautiful stunning website with a upload button
    for the chosen play.
    """
    if request.method == "POST":
        script = request.form['script']
        print(script)
        return redirect(url_for('speak', script=script))

if __name__ == "__main__":
    app.run()