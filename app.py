# app.py
from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/')
def login():
    name = request.args.get("name", "World")
    return render_template('login.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/forecast')
def forecast():
    return render_template('forecast.html')

@app.route('/login2')
def login2():
    return render_template('login2.html')

if __name__ == '__main__':
    app.run(debug=True)
