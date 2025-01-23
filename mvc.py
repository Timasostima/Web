from flask import Flask, request, jsonify, render_template

app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/services')
def services():
    return render_template("Services.html")


@app.route('/news')
def news():
    return render_template("News.html")


@app.route('/career')
def career():
    return render_template("Career.html")


@app.route('/about-us')
def about_us():
    return render_template("About-us.html")


@app.route('/contact')
def contact():
    return render_template("Contact.html")
