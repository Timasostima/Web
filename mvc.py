from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template("index.html")