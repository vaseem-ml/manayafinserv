from flask import Flask, request, jsonify, render_template, redirect, url_for, flash


app = Flask(__name__)



@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')


@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('home.html')