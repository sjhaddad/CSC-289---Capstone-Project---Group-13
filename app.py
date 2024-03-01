from flask import Flask, render_template, request, redirect, url_for, session
import bcrypt
from user_table_manager import User_table_manager
from tax_table_manager import Tax_table_manager
from tax_record import TaxRecord
from account import Account

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'  # Set a secret key for session management

user_table_manager = User_table_manager("database-2.cl6g04m6q6id.us-east-1.rds.amazonaws.com", "admin",
                                        "password",
                                        database="tax_program")
tax_table_manager = Tax_table_manager("database-2.cl6g04m6q6id.us-east-1.rds.amazonaws.com", "admin",
                                      "password",
                                      database="tax_program")


@app.route('/')
def index():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login():
    action = request.form['action']
    if action == 'Login':
        user_name = request.form['username']
        password = request.form['password']
        # Check if username and password are empty
        if not user_name.strip() or not password.strip():
            return "Username and password are required.", 400
        account = user_table_manager.get_account_by_user_name(user_name)
        # Perform login logic here
        if account:
            if bcrypt.checkpw(password.encode('utf-8'), account.get_password()):
                session['user_name'] = user_name  # Store the user's name in the session
                return render_template('user_interface.html')
            else:
                return "Access denied. Please try again."
    elif action == 'Create New Account':
        return render_template('create_account.html')


@app.route('/user_interface', methods=['POST'])
def user_interface():
    action = request.form['action']

    if action == 'display':
        user_name = session['user_name']

        account = user_table_manager.get_account_by_user_name(user_name)
        return render_template('display_user_info.html', account=account)
    elif action == 'edit':
        return render_template('edit_account.html')
    elif action == 'generate':
        return render_template('create_tax_record.html')
    else:
        # Handle invalid action (optional)
        return 'Invalid action', 400


@app.route('/display_account', methods=['POST'])
def display_account():
    return render_template('create_account.html')


@app.route('/calculate_tax', methods=['POST'])
def calculate_tax():
    if 'user_name' in session:  # Check if user_name is stored in the session
        user_name = session['user_name']  # Retrieve the user's name from the session
        year = request.form['year']
        status = request.form['status']
        total_income = float(request.form['income'])
        tax_record = TaxRecord(user_name, year, status, total_income)
        # Perform tax calculation and update tax table here
        tax_table_manager.add_tax_info(tax_record)
        tax_record.display_tax_info()
        return render_template('results.html', tax_record=tax_record)
    else:
        return redirect(url_for('index'))  # Redirect to login page if user is not logged in


@app.route('/create_account', methods=['POST'])
def create_account():
    user_name = request.form['username']
    password = request.form['password']
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    email = request.form['email']
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    if user_table_manager.get_account_by_user_name(user_name):
        return 'Username already exists. Please choose a different one.', 400
    else:
        session['user_name'] = user_name  # Store the user's name in the session

        new_account = Account(user_name, hashed_password, email, first_name, last_name)
        user_table_manager.add_user(new_account)
        return render_template('user_interface.html')


if __name__ == '__main__':
    app.run(debug=True)
