#!/usr/bin/env python3
from flask import Flask, render_template, url_for
from just_humidity import how_humid
app= Flask(__name__)

@app.route("/")
def home():
    h = how_humid()
    return render_template("main.html", h=h)

@app.route("/graph")
def graph():
    return render_template("graph.html")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0',port=5000)