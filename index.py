from flask import Flask, request, jsonify, render_template, redirect, url_for, flash
# from utils.helper import hash_password
import datetime
# # import ast
from src.services.db import User, Client, Admin
import bson
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
import bcrypt


user = User()
clients = Client()
admins = Admin()

app = Flask(__name__, template_folder='templates')
app.secret_key = "manaya-finserve"
login_manager = LoginManager()
login_manager.init_app(app)


class User_(UserMixin):
    def __init__(self, id, first_name, role):
        self.id = id
        self.username = first_name
        self.role = role


@login_manager.user_loader
def load_user(user_id):
    user_ = user.find_user({"_id": bson.ObjectId(user_id)})
    if user_:
        return User_(user_["_id"], user_['first_name'], user_['role'])
    return None



# @login_manager.unauthorized_handler
# def unauthorized():
#     return render_template('login.html')


# admin = admins.find_admin()
# if not admin:
#     admins.create_admin({
#             'email': 'aalam.manjoor718@gmail.com', 
#             'password': hash_password('password'), 
#             'mobile': '9828688097', 
#             'first_name': 'Manzoor',
#             'last_name': 'Aalam',
#             'role': 'admin',
#             'createdAt': datetime.datetime.now(),
#             'updatedAt': datetime.datetime.now()
#         })


# @app.route('/logout')
# @login_required
# def logout():
#     logout_user()
#     return redirect('/login')


@app.route('/login', methods=['GET', 'POST'])
def login():
    # if request.method=='POST':
    #     email = request.form["email"]
    #     role = request.form["role"]

    #     if not email:
    #         return jsonify({"error": "Please pass email address"}), 400
        
    #     if role=='admin':
    #         user_ = admins.find_admin({'email': email})
    #         print('this is admin', user_)
    #         if not user_:
    #             flash('User not found:error',)
    #             return redirect(url_for('login'))
    #         user_['role'] = 'admin'
    #     if role=='employee':
    #         user_ = user.find_user({'email': email})
    #         if not user_:
    #             flash('User not found:error',)
    #             return redirect(url_for('login'))
    #         user_['role']='employee'

    #     password = request.form["password"]
    #     hashed_password = user_["password"]
    #     if not bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8")):
    #         flash('Invalid username password combination:error')
    #         return redirect(url_for('login'))




    #     user_obj = User_(user_["_id"], user_['first_name'], user_['role'])

    #     login_user(user_obj)
    #     print('now everything is logged in++++++++++=============', user_obj)

    #     return redirect(url_for("home"))
    # if request.method=='GET':
        return render_template('login.html')

# @app.route('/home', methods=['GET', 'POST'])
# @login_required
# def home():
#     return render_template('home.html', user=current_user)


# @app.route('/employees', methods=['GET', 'POST'])
# def employees():
#     cond = { 'role': 'employee'}
#     if request.method == 'POST':
#         search = request.form["search"]
#         if search:
#             cond['search'] = search

#     users = user.get_users(cond)
#     users = list(users)

#     for index, user_ in enumerate(users):
#         users[index]['_id'] = str(user_['_id'])
#         # break
#     return render_template('employees.html', users=users, user=current_user)


# @app.route('/clients', methods=['GET', 'POST'])
# def get_clients():
#     cond = { }
#     if current_user.role=='employee':
#         cond = { 'employee': current_user.id }
#     if request.method == 'POST':
#         search = request.form["search"]
#         if search:
#             cond['search'] = search


#     clients_data = clients.get_clients(cond)
#     all_data = []
#     # for test in clients_data:
#     #     print('test++++++=======', test)
#     # clients_data = list(clients_data)

#     for index, user_ in enumerate(clients_data):
#         user_['_id'] = str(user_['_id'])
#         user_['employee'] = str(user_['employee'])
#         print('this is user', user_)
#         all_data.append(user_)
#         # break
#     return render_template('clients.html', clients=all_data, user=current_user)


# @app.route('/add-client', methods=['POST'])
# def add_client():
#     first_name = request.form["first_name"]
#     last_name = request.form["last_name"]
#     dob = request.form["dob"]
#     email = request.form["email"]
#     gender = request.form["gender"]


#     mobile = request.form["mobile"]
#     clientData = clients.find_client({ '$or': [{ 'email': email}, {'mobile': mobile}]})
#     if clientData:
#         flash('Email Or Mobile alreay exists. Try with other email!!!:error',)
#         return redirect(url_for('get_clients'))
#     data = {
#         'first_name': first_name,
#         'last_name': last_name,
#         'dob': dob,
#         'gender': gender,
#         'mobile': mobile,
#         'email': email,
#         'employee': bson.ObjectId(current_user.id),
#         'createdAt': datetime.datetime.now(), 
#         'updatedAt': datetime.datetime.now(), 
#     }
#     clients.create_client(data)
#     return redirect(url_for("get_clients"))

# @app.route('/client-details/<string:id>', methods=['GET'])
# def get_client(id):
#     print('this is id+++++=========', id)
#     client_detail = clients.find_client({'_id': bson.ObjectId(id)})
#     if not client_detail:
#         flash('Client not found:error',)
#         return redirect(url_for('get_clients'))


#     return render_template('components/client_details.html', client=client_detail, user=current_user)




# @app.route('/reports', methods=['GET', 'POST'])
# def reports():
#     return render_template('reports.html', user=current_user)


# @app.route('/add-employee', methods=['POST'])
# def add_employee():
#     first_name = request.form["first_name"]
#     last_name = request.form["last_name"]
#     designation = request.form["designation"]
#     dob = request.form["dob"]
#     email = request.form["email"]
#     gender = request.form["gender"]
#     status = request.form["status"]
#     password = request.form["password"]
#     if not password:
#         flash('password is empty:error',)
#         return redirect(url_for('employees'))

#     hashed_password = hash_password(password)
#     mobile = request.form["mobile"]
#     user_ = user.find_user({'email': email})
#     if user_:
#         flash('Email alreay exists. Try with other email!!!:error',)
#         return redirect(url_for('employees'))
#     data = {
#         'first_name': first_name,
#         'last_name': last_name,
#         'designation': designation,
#         'dob': dob,
#         'gender': gender,
#         'status': int(status),
#         'role': 'employee',
#         'mobile': mobile,
#         'password': hashed_password,
#         'email': email,
#         'createdAt': datetime.datetime.now(), 
#         'updatedAt': datetime.datetime.now(), 
#     }
#     user.create_user(data)
#     return redirect(url_for("employees"))

# @app.route('/edit-employee', methods=['POST'])
# def edit_employee():
#     _id = request.form['_id']
#     first_name = request.form["first_name"]
#     last_name = request.form["last_name"]
#     designation = request.form["designation"]
#     dob = request.form["dob"]
#     email = request.form["email"]
#     gender = request.form["gender"]
#     status = request.form["status"]
#     mobile = request.form["mobile"]
    
#     data = {
#         'first_name': first_name,
#         'last_name': last_name,
#         'designation': designation,
#         'dob': dob,
#         'gender': gender,
#         'status': int(status),
#         'role': 'employee',
#         'mobile': mobile,
#         'email': email,
#         'updatedAt': datetime.datetime.now(), 
#     }

#     user.update_user({'_id': bson.ObjectId(_id)}, data)
#     return redirect(url_for("employees"))

if __name__ == '__main__':
    app.run(debug=True)

    