from flask import Flask, request, jsonify, render_template, redirect, url_for, flash
from utils.helper import hash_password
import datetime
# import ast
from src.services.db import User, Client, Admin, Bank, Card, UserCard
import bson
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
import bcrypt


user = User()
clients = Client()
admins = Admin()
banks = Bank()
cards = Card()
user_cards = UserCard()


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
    if not user_:
        user_ = admins.find_admin({"_id": bson.ObjectId(user_id)})
    
    if user_:
        return User_(user_["_id"], user_['first_name'], user_['role'])
    
    return None



@login_manager.unauthorized_handler
def unauthorized():
    return render_template('login.html')


admin = admins.find_admin()
if not admin:
    admins.create_admin({
            'email': 'aalam.manjoor718@gmail.com', 
            'password': hash_password('password'), 
            'mobile': '9828688097', 
            'first_name': 'Manzoor',
            'last_name': 'Aalam',
            'role': 'admin',
            'createdAt': datetime.datetime.now(),
            'updatedAt': datetime.datetime.now()
        })


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/login')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method=='POST':
        email = request.form["email"]
        role = request.form["role"]

        if not email:
            return jsonify({"error": "Please pass email address"}), 400
        
        if role=='admin':
            user_ = admins.find_admin({'email': email})
            if not user_:
                flash('User not found:error',)
                return redirect(url_for('login'))
            user_['role'] = 'admin'
        if role=='employee':
            user_ = user.find_user({'email': email})
            if not user_:
                flash('User not found:error',)
                return redirect(url_for('login'))
            user_['role']='employee'

        password = request.form["password"]
        hashed_password = user_["password"]
        if not bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8")):
            flash('Invalid username password combination:error')
            return redirect(url_for('login'))
        
        print('everything going good++++++++++++++===============', user_)

        user_obj = User_(user_["_id"], user_['first_name'], user_['role'])

        login_user(user_obj)
        print('now everything is logged in++++++++++=============', current_user.username)

        return redirect(url_for("home"))
    if request.method=='GET':
        return render_template('login.html')

@app.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    return render_template('userview.html', user=current_user)


@app.route('/employees', methods=['GET', 'POST'])
@login_required
def employees():
    cond = { 'role': 'employee'}
    if request.method == 'POST':
        search = request.form["search"]
        if search:
            cond['search'] = search

    users = user.get_users(cond)
    users = list(users)

    for index, user_ in enumerate(users):
        users[index]['_id'] = str(user_['_id'])
        # break
    return render_template('employees.html', users=users, user=current_user)


@app.route('/clients', methods=['GET', 'POST'])
@login_required
def get_clients():
    cond = { }
    if current_user.role=='employee':
        cond = { 'employee': current_user.id }
    if request.method == 'POST':
        search = request.form["search"]
        if search:
            cond['search'] = search


    clients_data = clients.get_clients(cond)
    

    all_data = []


    for index, user_ in enumerate(clients_data):
        user_['_id'] = str(user_['_id'])
        user_['employee'] = str(user_['employee'])
        all_data.append(user_)
    return render_template('clients.html', clients=all_data, user=current_user)

@app.route('/add-client', methods=['POST'])
@login_required
def add_client():
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    dob = request.form["dob"]
    email = request.form["email"]
    gender = request.form["gender"]


    mobile = request.form["mobile"]
    clientData = clients.find_client({ '$or': [{ 'email': email}, {'mobile': mobile}]})
    if clientData:
        flash('Email Or Mobile alreay exists. Try with other email!!!:error',)
        return redirect(url_for('get_clients'))
    data = {
        'first_name': first_name,
        'last_name': last_name,
        'dob': dob,
        'gender': gender,
        'mobile': mobile,
        'email': email,
        'employee': bson.ObjectId(current_user.id),
        'createdAt': datetime.datetime.now(), 
        'updatedAt': datetime.datetime.now(), 
    }
    clients.create_client(data)
    return redirect(url_for("get_clients"))

@app.route('/client-details/<string:id>', methods=['GET'])
def get_client(id):
    
    client_detail = clients.find_client({'_id': bson.ObjectId(id)})

    if not client_detail:
        flash('Client not found:error',)
        return redirect(url_for('get_clients'))
    

    
    banks_data = banks.get_bank_with_cards()
    # print('this is banks data', list(banks_data))
    banks_data = list(banks_data)
    users_data = user.get_users()
    users_data = list(users_data)
    for index, bank_ in enumerate(banks_data):
        banks_data[index]['_id'] = str(bank_['_id'])

    client_cards = user_cards.get_client_cards({"client": bson.ObjectId(id)})
    # for index, client_card in enumerate(client_cards):
        
    

    # print('this is client detail', list(client_cards))



    return render_template('components/client_details.html', 
                           client=client_detail, 
                           banks=banks_data,
                           users = users_data,
                           client_cards = client_cards,
                           user=current_user)

@app.route('/add-card', methods=['POST'])
def add_card():
    card = request.form["card"]
    client = request.form["client"]
    status = request.form["status"]
    employees = request.form.getlist('employees')

    print('these are the employees', employees)
    
    users=[]
    for employee in employees:
        users.append({'employee': bson.ObjectId(employee)})
    
    data = {
        'card': bson.ObjectId(card),
        'client': bson.ObjectId(client),
        'status': status,
        'employees': users,
        'createdAt': datetime.datetime.now(), 
        'updatedAt': datetime.datetime.now(), 
    }
    user_cards.create_user_card(data)
    return redirect(url_for("get_clients"))



@app.route('/edit-card', methods=['POST'])
def edit_user_card():
    card = request.form["card"]
    _id = request.form['edit_card_id']
    #client = request.form["client"]
    status = request.form["status"]
    employees = request.form.getlist('employees')

    users=[]
    for employee in employees:
        users.append({'employee': bson.ObjectId(employee)})
    
    data = {
        'card': bson.ObjectId(card),
        #'client': bson.ObjectId(client),
        'status': status,
        'employees': users,
        #'createdAt': datetime.datetime.now(), 
        'updatedAt': datetime.datetime.now(), 
    }
    user_cards.update_user_card({'_id': bson.ObjectId(_id)}, data)
    return redirect(url_for("get_clients"))



@app.route('/reports', methods=['GET', 'POST'])
@login_required
def reports():
    cond={}
    if request.method == 'POST':
        search = request.form["search"]
        from_ = request.form["from"]
        to = request.form["to"]
        card = request.form["card"]
        if search:
            cond['search'] = search

    get_default_cards = cards.get_cards()
    get_default_cards = list(get_default_cards)

    data = {
        "cards": get_default_cards
    }

    if current_user.role=='employee':
        cond["$expr"] = {
                "$in": [bson.ObjectId(current_user.id), "$employees.employee"],
            },
    client_cards = user_cards.get_all_cards(cond)


    


    client_cards = list(client_cards)
    return render_template('reports.html', cards = client_cards, data=data, user=current_user)


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

@app.route('/edit-employee', methods=['POST'])
def edit_employee():
    _id = request.form['_id']
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    designation = request.form["designation"]
    dob = request.form["dob"]
    email = request.form["email"]
    gender = request.form["gender"]
    status = request.form["status"]
    mobile = request.form["mobile"]
    
    data = {
        'first_name': first_name,
        'last_name': last_name,
        'designation': designation,
        'dob': dob,
        'gender': gender,
        'status': int(status),
        'role': 'employee',
        'mobile': mobile,
        'email': email,
        'updatedAt': datetime.datetime.now(), 
    }

    user.update_user({'_id': bson.ObjectId(_id)}, data)
    return redirect(url_for("employees"))



@app.route('/banks', methods=['GET', 'POST'])
@login_required
def get_banks():
    cond= {}
    if request.method == 'POST':
        search = request.form["search"]
        if search:
            cond['search'] = search

    banks_data = banks.get_banks(cond)

    banks_data = list(banks_data)
    for index, bank_ in enumerate(banks_data):
        banks_data[index]['_id'] = str(bank_['_id'])
    return render_template('banks.html', banks=banks_data, user=current_user)

@app.route('/add-bank', methods=['POST'])
def add_bank():
    name = request.form["name"]
    status = request.form["status"]
    
    bank_ = banks.find_bank({'name': name})
    if bank_:
        flash('Bank alreay exists!!!:error',)
        return redirect(url_for('get_banks'))
    data = {
        'name': name,
       
        'status': int(status),
        
        'createdAt': datetime.datetime.now(), 
        'updatedAt': datetime.datetime.now(), 
    }
    banks.create_bank(data)
    return redirect(url_for("get_banks"))


@app.route('/edit-bank', methods=['POST'])
def edit_bank():
    try:
        _id = request.form['_id']
        name = request.form["name"]

        status = request.form["status"]
        
        data = {
            'first_name': name,


            'status': int(status),

            'updatedAt': datetime.datetime.now(), 
        }

        banks.update_bank({'_id': bson.ObjectId(_id)}, data)
        return redirect(url_for("get_banks"))
    except Exception as e:
        flash(f'str{e}:error',)
        return redirect(url_for('get_banks'))

@app.route('/cards', methods=['GET', 'POST'])
@login_required
def get_cards():
    cond= {}
    if request.method == 'POST':
        search = request.form["search"]
        if search:
            cond['search'] = search

    cards_data = cards.get_cards(cond)

    bank_data = banks.get_banks()
    bank_data = list(bank_data)
    for index, bank_ in enumerate(bank_data):
        bank_data[index]['_id'] = str(bank_['_id'])

    cards_data = list(cards_data)
    for index, card_ in enumerate(cards_data):
        cards_data[index]['_id'] = str(card_['_id'])
    print('these are cards', cards_data)
    
    return render_template('cards.html', cards=cards_data,banks=bank_data, user=current_user)

@app.route('/add-bank-card', methods=['POST'])
def add_bank_card():
    name = request.form["name"]
    bank = request.form["bank"]
    status = request.form["status"]
    
    card_ = cards.find_card({'name': name})
    if card_:
        flash('card alreay exists!!!:error',)
        return redirect(url_for('get_cards'))
    data = {
        'name': name,
        'bank': bson.ObjectId(bank),
        'status': int(status),
        
        'createdAt': datetime.datetime.now(), 
        'updatedAt': datetime.datetime.now(), 
    }
    cards.create_card(data)
    return redirect(url_for("get_cards"))


@app.route('/edit-bank-card', methods=['POST'])
def edit_card():
    try:
        _id = request.form['_id']
        bank = request.form['bank']
        name = request.form["name"]

        status = request.form["status"]
        
        data = {
            'first_name': name,
            'bank': bson.ObjectId(bank),

            'status': int(status),

            'updatedAt': datetime.datetime.now(), 
        }

        cards.update_card({'_id': bson.ObjectId(_id)}, data)
        return redirect(url_for("get_cards"))
    except Exception as e:
        flash(f'str{e}:error',)
        return redirect(url_for('get_cards'))




if __name__ == '__main__':
    app.run(debug=True)

    