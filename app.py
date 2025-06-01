from flask import Flask, request, render_template, session, redirect, url_for, jsonify
import sqlite3
import secrets
import telepot
import os
from main import infer_by_web
from main import process_image
app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

connection = sqlite3.connect('database.db')
cursor = connection.cursor()

command = """CREATE TABLE IF NOT EXISTS user (Id INTEGER PRIMARY KEY AUTOINCREMENT, fname TEXT, lname TEXT, phone TEXT, email TEXT, password TEXT)"""
cursor.execute(command)

def predict_image(path, type):
    print(path)
    return infer_by_web(path, type)


@app.route("/")
def index():
    return render_template("login.html")

@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()

        email = request.form['email']
        password = request.form['password']

        query = "SELECT * FROM user WHERE email = '"+email+"' AND password= '"+password+"'"
        cursor.execute(query)
        result = cursor.fetchone()

        if result:
            session['user'] = result
            return render_template("home.html")
        else:
            return render_template("login.html", msg="Entered wrong credentials")        
    return render_template("login.html")

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        fname = request.form['fname']
        lname = request.form['lname']
        phone = request.form['phone']
        email = request.form['email']
        password = request.form['password']

        cursor.execute("INSERT INTO user VALUES (NULL, '"+fname+"', '"+lname+"', '"+phone+"', '"+email+"', '"+password+"')")
        connection.commit()

        return render_template("login.html", msg="Registered successfully")
    return render_template("login.html")

@app.route("/recognition", methods=['GET', 'POST'])
def recogntion():
    if request.method == 'POST':
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()

        Image = request.form['image']
        option = 'bestPath'
        path = 'static/test/'+Image
        result = predict_image(path, option)
        print("Prediction: ", result)
        extracted_text = process_image(path)
        return render_template("recognition.html", result=extracted_text, image = path)
    return render_template("recognition.html")

@app.route("/logout")
def logout():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
