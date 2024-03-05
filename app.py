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


# Landing page, prompting user to login or create an account **COMPLETED FOR TESTING**
@app.route('/', methods=["GET", "POST"])
def index():
    error_message = ""
    if request.method == "POST":
        # User chooses to log in
        if "login_button" in request.form:
            user_name = request.form['username']
            password = request.form['password']
            # Check if username and password are empty
            if not user_name.strip() or not password.strip():
                error_message = "Username and password are required."
            account = user_table_manager.get_account_by_user_name(user_name)
            # Perform login logic here
            if account:
                if bcrypt.checkpw(password.encode('utf-8'), account.get_password()):
                    session['user_name'] = user_name
                    return redirect(url_for('user_interface'))
                else:
                    error_message = "Invalid credentials. Please try again."

        # User chooses to create new account
        elif "create_button" in request.form:
            return redirect(url_for('create_account'))

    return render_template("index.html", error_message=error_message)


# Account creation page **COMPLETED FOR TESTING**
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
            session['user_name'] = user_name  # Store the user's name in the session
            new_account = Account(user_name, hashed_password, email, first_name, last_name)
            user_table_manager.add_user(new_account)
            return redirect(url_for('user_interface'))

    return render_template('create_account.html', error_message=error_message)


'''
** USER MODE PAGES ** 
'''


# User interface page, presenting end user with option to display their information, edit their information, or generate their tax estimate **COMPLETED FOR TESTING**
@app.route('/user_interface', methods=["GET", "POST"])
def user_interface():
    error_message = ""
    if request.method == "POST":
        if "redirect_submit" in request.form:
            redirection = request.form["redirection"]
            if redirection == "display":
                return redirect(url_for("user_display"))
            elif redirection == "edit":
                return redirect(url_for('edit_account'))
            elif redirection == "generate":
                return redirect(url_for('calculate_tax'))
            else:
                # Handle invalid action (optional)
                error_message = 'Invalid action'

    return render_template('user_interface.html', error_message=error_message)


# User account information display page, showing the user their account information and any tax records if they exist **COMPLETED FOR TESTING**
@app.route('/user_display', methods=["GET", "POST"])
def user_display():
    user_name = session['user_name']
    account = user_table_manager.get_account_by_user_name(user_name)
    tax_records = tax_table_manager.get_tax_records(user_name)
    return render_template('user_display.html', account=account, tax_records=tax_records)


# User account information edit page, allowing the user to edit their account information **COMPLETED FOR TESTING**
@app.route('/edit_account', methods=["GET", "POST"])
def edit_account():
    if request.method == "POST":
        user_name = session.get('user_name')
        account = user_table_manager.get_account_by_user_name(user_name)

        # Update the account fields if they are provided and not empty in the form
        if 'email' in request.form and request.form['email'].strip():
            account.set_email(request.form['email'])
        if 'first_name' in request.form and request.form['first_name'].strip():
            account.set_first_name(request.form['first_name'])
        if 'last_name' in request.form and request.form['last_name'].strip():
            account.set_last_name(request.form['last_name'])
        if 'password' in request.form and request.form['password'].strip():
            hashed_password = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt())
            account.set_password(hashed_password)

        # Update the user account if any fields are provided
        if any(field in request.form and request.form[field].strip() for field in
               ['email', 'first_name', 'last_name', 'password']):
            user_table_manager.update_user(account)

        # Redirect back to the user interface page
        return redirect(url_for('user_interface'))

    # If the request method is not POST, render the edit_account.html template
    return render_template('edit_account.html')


# User tax record creation page, allowing user to generate their tax estimate **COMPLETED FOR TESTING**
@app.route('/calculate_tax', methods=["GET", "POST"])
def calculate_tax():
    if 'user_name' in session:  # Check if user_name is stored in the session
        user_name = session['user_name']  # Retrieve the user's name from the session
        if request.method == "POST":

            year = request.form['year']
            status = request.form['status']
            total_income = float(request.form['income'])
            tax_record = TaxRecord(user_name, year, status, total_income)
            # Perform tax calculation and update tax table here

            if tax_table_manager.is_year_unique(user_name, year):
                tax_table_manager.add_tax_info(tax_record)
                return render_template('results.html', tax_record=tax_record)
            else:
                error_message = "Tax record already exists for this year."
                return render_template('calculate_tax.html', error_message=error_message)


        return render_template('calculate_tax.html')



'''
** ADMIN MODE PAGES **
'''

if __name__ == '__main__':
    app.run(debug=True)
    #user_table_manager.display_table()
    #tax_table_manager.display_table()
