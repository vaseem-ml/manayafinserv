from flask import Flask, request, jsonify, render_template, redirect, url_for, flash
from utils.helper import hash_password
import datetime
import ast
from src.services.db import User
import bson
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
import bcrypt


user = User()

app = Flask(__name__, template_folder='templates')
app.secret_key = "manaya-finserve"
login_manager = LoginManager()
login_manager.init_app(app)


class User_(UserMixin):
    def __init__(self, id, name, role):
        self.id = id
        self.username = name
        self.role = role


@login_manager.user_loader
def load_user(user_id):
    user_ = user.find_user({"_id": bson.ObjectId(user_id)})
    if user_:
        return User_(user_["_id"], user_['name'], user_['role'])
    return None


admin = user.find_user({'role': 'admin'})
if not admin:
    user.create_user({
            'email': 'aalam.manjoor718@gmail.com', 
            'password': hash_password('password'), 
            'mobile': '9828688097', 
            'name': 'Manzoor Aalam',
            'role': 'admin',
            'createdAt': datetime.datetime.now(),
            'updatedAt': datetime.datetime.now()
        })


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method=='POST':
        email = request.form["email"]
        if not email:
            return jsonify({"error": "Please pass email address"}), 400

        user_ = user.find_user({'email': email})
        if not user_:
            flash('User not found:error',)
            return redirect(url_for('login'))

        password = request.form["password"]
        hashed_password = user_["password"]
        if not bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8")):
            flash('Invalid username password combination:error')
            return redirect(url_for('login'))



        user_obj = User_(user_["_id"], user_['name'], user_['role'])
        login_user(user_obj)
        return redirect(url_for("home"))
    if request.method=='GET':
        return render_template('login.html')


@app.route('/home', methods=['GET', 'POST'])
def home():
    return render_template('home.html', user=current_user)


@app.route('/employees', methods=['GET', 'POST'])
def employees():
    cond = { 'role': 'employee'}
    if request.method == 'POST':
        search = request.form["search"]
        if search:
            cond['search'] = search

    users = user.get_users(cond)
    return render_template('employees.html', users=users, user=current_user)


@app.route('/reports', methods=['GET', 'POST'])
def reports():
    return render_template('reports.html', user=current_user)



@app.route('/add-employee', methods=['POST'])
def add_employee():
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    designation = request.form["designation"]
    dob = request.form["dob"]
    email = request.form["email"]
    gender = request.form["gender"]
    status = request.form["status"]
    password = request.form["password"]
    if not password:
        flash('password is empty:error',)
        return redirect(url_for('employees'))

    hashed_password = hash_password(password)
    mobile = request.form["mobile"]
    user_ = user.find_user({'email': email})
    if user_:
        flash('Email alreay exists. Try with other email!!!:error',)
        return redirect(url_for('employees'))
    data = {
        'first_name': first_name,
        'last_name': last_name,
        'designation': designation,
        'dob': dob,
        'gender': gender,
        'status': int(status),
        'role': 'employee',
        'mobile': mobile,
        'password': hashed_password,
        'email': email,
        'createdAt': datetime.datetime.now(), 
        'updatedAt': datetime.datetime.now(), 
    }
    user.create_user(data)
    return redirect(url_for("employees"))



# if __name__ == '__main__':
#     app.run(debug=True)

    