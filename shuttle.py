from flask import Flask, render_template, request, redirect, url_for, session
import bcrypt
import uuid
from datetime import datetime, timedelta
from user_table_manager import User_table_manager
from tax_table_manager import Tax_table_manager
from tax_record import TaxRecord
from account import Account
from flask_mail import Mail, Message
from constants import *
from flaskwebgui import FlaskUI

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'  # Set a secret key for session management

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'shuttlecash919@gmail.com'
app.config['MAIL_PASSWORD'] = 'buyp yinf yyrw ymye'

mail = Mail(app)

user_table_manager = User_table_manager("database-2.cl6g04m6q6id.us-east-1.rds.amazonaws.com", "admin",
                                        "password",
                                        database="tax_program")
tax_table_manager = Tax_table_manager("database-2.cl6g04m6q6id.us-east-1.rds.amazonaws.com", "admin",
                                      "password",
                                      database="tax_program")
password_reset_tokens = {}

#### NON-LOGGED IN PAGES ####
'''
Home page, prompting user to either login using credentials stored in the database, or create a new account. 
User is redirected to /user_interface if correct credentials associated with non-admin account are entered, /admin_home if admin account, 
and /create_account if selecting to create account.
'''


@app.route('/', methods=["GET", "POST"])
def index():
    session.clear()
    error_message = ""
    if request.method == "POST":
        if "login-button" in request.form:
            user_name = request.form['username']
            password = request.form['password']
            print(user_name == "")
            if user_name != "" and password != "":

                account = user_table_manager.get_account_by_user_name(user_name)
                if account:
                    if bcrypt.checkpw(password.encode('utf-8'), account.get_password()) and user_name != "admin":
                        session['user_name'] = user_name
                        return redirect(url_for('user_interface'))
                    elif bcrypt.checkpw(password.encode('utf-8'), account.get_password()) and user_name == "admin":
                        session['user_name'] = user_name
                        return redirect(url_for('admin_home'))
                    else:
                        error_message = "Incorrect password. Please try again."
                else:
                    error_message = "Invalid user name"
            else:
                error_message = "Username and password are required."
        elif "create_button" in request.form:
            return redirect(url_for('create_account'))

        elif "details" in request.form:
            return redirect(url_for('details'))

    return render_template("index.html", error_message=error_message)


'''
Create account page, accepting input for username, password, email, first name, and last name to create a new account stored in the user table.
Redirects to /user_interface upon successful account creation.
'''
@app.route('/create_account', methods=["GET", "POST"])
def create_account():
    error_message = ""
    if request.method == "POST":
        user_name = request.form['username']
        password = request.form['password']
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        email = request.form['email']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        if user_table_manager.get_account_by_user_name(user_name):
            error_message = 'Username already exists. Please choose a different one.'
        else:
            session['user_name'] = user_name
            new_account = Account(user_name, hashed_password, email, first_name, last_name)
            user_table_manager.add_user(new_account)
            return redirect(url_for('user_interface'))

    return render_template('create_account.html', error_message=error_message)


@app.route('/request_password_reset', methods=['GET', 'POST'])
def request_password_reset():
    error_message = ""
    if request.method == "POST":
        subject = 'Password Reset'  # Set the subject directly
        recipient = request.form['email']
        if user_table_manager.get_account_by_email(recipient):
            session['email'] = recipient
            token = str(uuid.uuid4())
            body = f"Click the following link to reset your password: {url_for('password_reset_link', token=token, _external=True)}"
            msg = Message(subject=subject, sender='shuttlecash919@gmail.com', recipients=[recipient])
            msg.body = body
            mail.send(msg)
            return 'Check email for reset link!'

        else:
            error_message = "Email not in system. "
            # return redirect(url_for('index'))

    return render_template("request_password_reset.html", error_message=error_message)


@app.route('/password_reset_link', methods=['GET', 'POST'])
def password_reset_link():
    account = user_table_manager.get_account_by_email(session.get('email'))

    if request.method == "POST":
        error_message = ''
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']
        if new_password == confirm_password:
            hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())

            account.set_password(hashed_password)
            user_table_manager.update_user(account)
            error_message = 'Password updated.'
            return redirect(url_for('index'))
        else:
            error_message = "Error: New password and confirm password do not match. Please try again."
            return render_template('password_reset_link.html', account=account, error_message=error_message)

    return render_template('password_reset_link.html', account=account)

@app.route('/details')
def details():
    return render_template('details.html')


#### USER ACCOUNT PAGES ####
'''
User interface page, redirecting to /user_display, /edit_account, /calculate_tax, and / based on user selection.
'''


@app.route('/user_interface', methods=["GET", "POST"])
def user_interface():
    if not session:
        return redirect(url_for('index'))

    message = request.args.get('message')
    if message is None:
        message = ""
    if request.method == "POST":
        print("redirect_submit" in request.form)
        if "redirect_submit" in request.form:
            redirection = request.form["redirection"]
            print(redirection)
            if redirection == "display":
                return redirect(url_for("user_display"))
            elif redirection == "edit":
                return redirect(url_for('edit_account'))
            elif redirection == "generate":
                return redirect(url_for('deduction'))
        if 'logout' in request.form:
            session.clear()
            return redirect(url_for('index'))

    return render_template('user_interface.html', message=message)


'''
User display page, displaying the information associated with the signed-in user. Displays user account info, and tax records
if present. Redirects to /user_interface when "Return Home" button is clicked.
'''


@app.route('/deduction', methods=['GET', 'POST'])
def deduction():
    if request.method == 'POST':
        deduction_type = request.form.get('deduction_type')
        session['deduction_type'] = deduction_type

        if deduction_type == 'standard':
            return redirect(url_for('calculate_tax'))
        elif deduction_type == 'itemized':
            return redirect(url_for('itemized_deduction'))

    return render_template('deduction.html')


@app.route('/itemized_deduction', methods=['GET', 'POST'])
def itemized_deduction():
    if request.method == "POST":
        if "next" in request.form:
            charitable_contributions = float(request.form["charitable_contributions"])
            mortgage_interest = float(request.form["mortgage_interest"])
            medical_expenses = float(request.form["medical_expenses"])
            other_expenses = float(request.form["other_expenses"])
            deductible = charitable_contributions + mortgage_interest + medical_expenses + other_expenses
            session['deductible'] = deductible

            return redirect(url_for('calculate_tax'))
        elif "return_home" in request.form:
            return redirect(url_for('user_interface'))

    return render_template("itemized_deduction.html")


@app.route('/user_display', methods=["GET", "POST"])
def user_display():
    user_name = session.get('user_name')
    if not user_name:
        return redirect(url_for('index'))

    account = user_table_manager.get_account_by_user_name(user_name)
    tax_records = tax_table_manager.get_tax_records(user_name)
    if request.method == "POST":
        if "return_home" in request.form:
            return redirect(url_for('user_interface'))

    return render_template('user_display.html', account=account, tax_records=tax_records)


'''
Edit account page, allowing user to change the email, first name, last name, or password associated with their account.
Stores changes in user table, redirects to /user_interface if "Return Home" button is pressed or upon succesful info update.
'''


@app.route('/edit_account', methods=["GET", "POST"])
def edit_account():
    user_name = session.get('user_name')
    if not user_name:
        return redirect(url_for('index'))

    account = user_table_manager.get_account_by_user_name(user_name)
    if request.method == "POST":
        if "edit_submit" in request.form:
            if 'email' in request.form and request.form['email'].strip():
                account.set_email(request.form['email'])
            if 'first_name' in request.form and request.form['first_name'].strip():
                account.set_first_name(request.form['first_name'])
            if 'last_name' in request.form and request.form['last_name'].strip():
                account.set_last_name(request.form['last_name'])
            if 'password' in request.form and request.form['password'].strip():
                hashed_password = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt())
                account.set_password(hashed_password)

            if any(field in request.form and request.form[field].strip() for field in
                   ['email', 'first_name', 'last_name', 'password']):
                user_table_manager.update_user(account)
                message = "Account updated."
                return redirect(url_for('user_interface', message=message))

        elif "return_home" in request.form:
            return redirect(url_for('user_interface'))

    return render_template('edit_account.html')


'''
Tax calculator page, allowing user to enter year, marital status, and total income to generate a tax record for them.
Redirects to /user_interface if "Return Home" button selected. Renders results.html if record generation successful.
'''


@app.route('/calculate_tax', methods=["GET", "POST"])
def calculate_tax():
    user_name = session.get('user_name')
    if not user_name:
        return redirect(url_for('index'))

    if request.method == "POST":
        if "calculate_submit" in request.form:
            year = request.form['year']
            status = request.form['status']
            total_income = float(request.form['income'])
            if session['deduction_type'] == "standard":
                if status == 'married' and total_income > 22500:
                    deductible = MARRIED_DEDUCTIBLE
                elif status == 'single' and total_income > 12750:
                    deductible = SINGLE_DEDUCTIBLE
                else:
                    deductible = 0

                tax_record = TaxRecord(user_name, year, status, total_income, deductible)


            elif session['deduction_type'] == "itemized":
                deductible = session["deductible"]
                tax_record = TaxRecord(user_name, year, status, total_income, deductible)

            if tax_table_manager.is_year_unique(user_name, year):
                tax_table_manager.add_tax_info(tax_record)
                return render_template('results.html', tax_record=tax_record)
            else:
                error_message = "Tax record already exists for this year."
                return render_template('calculate_tax.html', error_message=error_message)


        elif "return_home" in request.form:
            return redirect(url_for('user_interface'))

    return render_template('calculate_tax.html')


'''
Tax record results page, allowing user to see the output of a successful tax record generation.
Redirects to /user_interface if "Return Home" button selected.
'''


@app.route('/results', methods=["GET", "POST"])
def results():
    if request.method == "POST":
        if "return_home" in request.form:
            return redirect(url_for('user_interface'))

    return render_template('results.html')


#### ADMIN ACCOUNT PAGES ####
'''
Admin home page, redirecting to /all_users_display, /user_by_username, /delete_user, and / based on user selection.
'''


@app.route('/admin_home', methods=["GET", "POST"])
def admin_home():
    # Check to ensure that page is being accessed by an admin user, redirect to login if not
    if not session or session.get('user_name') != 'admin':
        return redirect(url_for('index'))

    error_message = ""
    if request.method == "POST":
        if "redirect_submit" in request.form:
            redirection = request.form["redirection"]
            if redirection == "all_users":
                return redirect(url_for("all_users_display"))
            elif redirection == "by_name":
                return redirect(url_for('user_by_username'))
            elif redirection == "delete_user":
                return redirect(url_for('delete_user'))
        elif 'logout' in request.form:
            session.clear()
            return redirect(url_for('index'))

    return render_template('admin_home.html', error_message=error_message)


'''
All user information display page, displaying all information for every user in two tables. This includes
user information as well as tax records. Redirects to /admin_home if "Return Home" button selected.
'''


@app.route('/all_users_display', methods=["GET", "POST"])
def all_users_display():
    # Check to ensure that page is being accessed by an admin user, redirect to login if not
    if not session or session.get('user_name') != 'admin':
        return redirect(url_for('index'))

    # Instantiate dictionary variables using table manager functions in order to pass to the template for display
    user_data_dict = user_table_manager.get_user_dict()
    tax_data_dict = tax_table_manager.get_tax_dict()
    if request.method == "POST":
        if "return_home" in request.form:
            return redirect(url_for("admin_home"))

    return render_template('all_users_display.html', user_data=user_data_dict, tax_data=tax_data_dict)


'''
Display user by username page, displaying information associated with a user that is specified by input of their username.
Redirects to /admin_home if "Return Home" button is selected.
'''


@app.route('/user_by_username', methods=["GET", "POST"])
def user_by_username():
    # Check to ensure that page is being accessed by an admin user, redirect to login if not
    if not session or session.get('user_name') != 'admin':
        return redirect(url_for('index'))

    # Declare generic versions of variables to pass to template in case of "if" statements never executing
    account = Account("N/A", "N/A", "N/A", "N/A", "N/A")
    tax_records = []

    if request.method == "POST":
        if "search_user" in request.form:
            search_name = request.form['search_name']
            account = user_table_manager.get_account_by_user_name(search_name)
            tax_records = tax_table_manager.get_tax_records(search_name)
        if "return_home" in request.form:
            return redirect(url_for("admin_home"))

    return render_template('user_by_username.html', user_data=account, tax_data=tax_records,
                           tax_data_size=len(tax_records))


'''
Delete user page, allowing admin to delete a user from database by specifying the user's name.
Redirects to /admin_home if "Return Home" button is selected.
'''


@app.route('/delete_user', methods=["GET", "POST"])
def delete_user():
    # Check to ensure that page is being accessed by an admin user, redirect to login if not
    if not session or session.get('user_name') != 'admin':
        return redirect(url_for('index'))

    feedback = ""
    if request.method == "POST":
        if "delete_user" in request.form:
            delete_name = request.form['delete_name']
            account = user_table_manager.get_account_by_user_name(delete_name)
            if account:
                user_table_manager.delete_user(delete_name)
                tax_table_manager.delete_record(delete_name)
                feedback = "User deleted."
            else:
                feedback = "User not found."
        if "return_home" in request.form:
            return redirect(url_for("admin_home"))

    return render_template('delete_user.html', feedback_message=feedback)


if __name__ == '__main__':
    FlaskUI(app=app, server="flask").run()
