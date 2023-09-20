from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template('home.html')


@app.route("/about")
def about():
    return render_template('about.html')


@app.route("/lorem")
def lorem():
    return render_template('lorem.html')


@app.route("/demo_eye")
def demo_eye():
    from . import EyeTracker
    return render_template('demo_eye.html')


@app.route("/demo_hand")
def demo_hand():
    from . import HandTracker