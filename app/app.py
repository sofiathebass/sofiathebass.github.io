from flask import Flask, request, jsonify, render_template, redirect, url_for, session
# from flask_cors import CORS

app = Flask(__name__)
app.secret_key = "super secret key"
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
    data = {}
    data['script'] = request.args.get('script')
    session['script'] = data['script']
    return render_template("app/speak.html", data=data)


@app.route("/uploadLine", methods=["POST"])
def uploadLine():
    """
    The upload page for our beautiful stunning website with a upload button
    for the chosen play.
    """
    if request.method == "POST":
        script = request.form['script']
        return redirect(url_for('speak', script=script))


@app.route("/uploadAudio", methods=["POST"])
def uploadAudio():
    if request.method == "POST":
        f = request.files['audio_data']
        with open('audio.wav', 'wb') as audio:
            suggested_sentiment, user_sentiment = runModel(audio, session['script'])
            session['suggested_sentiment'] = suggested_sentiment
            session['user_sentiment'] = user_sentiment
            return redirect(url_for('showResult'))


@app.route("/showResult")
def showResult():
    data = {}
    data['suggested_sentiment'] = session['suggested_sentiment']
    data['user_sentiment'] = session['user_sentiment']
    return render_template("app/result.html", data=data)


# @app.route("/runModel", methods=["POST"])
def runModel(audio, script):
    # TODO Get audio file
    print(audio)
    print(script)
    return 1, 1


if __name__ == "__main__":
    app.run()