from account import Account
from user_table_manager import User_table_manager
from tax_table_manager import Tax_table_manager
from tax_record import TaxRecord
import customtkinter as ctk
from constants import *
from input_validator import *
import bcrypt


class Interface:
    def __init__(self):
        self.user_table_manager = User_table_manager("database-2.cvi44qi26x3h.us-east-2.rds.amazonaws.com", "admin",
                                             "mypassword",
                                             database="new_tax_table")
        self.tax_table_manager = Tax_table_manager("database-2.cvi44qi26x3h.us-east-2.rds.amazonaws.com", "admin",
                                           "mypassword",
                                           database="new_tax_table")
        self.root = ctk.CTk()
        self.root.geometry("500x350")
        self.current_frame = None
        
    # Landing page GUI
    def landing_page(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("green")

        login_frame = ctk.CTkFrame(master=self.root)
        login_frame.pack(pady=20, padx=60, fill="both", expand=True)
        self.current_frame = login_frame

        label = ctk.CTkLabel(master=login_frame, text="Login system")
        label.pack(pady=12, padx=10)

        user_name = ctk.CTkEntry(master=login_frame, placeholder_text="Username")
        user_name.pack(pady=12, padx=10)

        password = ctk.CTkEntry(master=login_frame, placeholder_text="Password", show="*")
        password.pack(pady=12, padx=10)

        button = ctk.CTkButton(master=login_frame, text="Login", command=lambda: self.login(user_name, password, label))
        button.pack(pady=12, padx=10)

        self.root.mainloop()

    # Backend logic for Landing page
    def login(self, name_input, pass_input, label):
        user_name = name_input.get()
        password = pass_input.get()

        if user_name == "admin" and password == "admin":
            account = Account("admin", "admin", None, None, None)
            label.configure(text="Login successful")
            self.admin_screen(account)

        account = self.user_table_manager.get_account_by_user_name(user_name)
        if account:
            if bcrypt.checkpw(password.encode('utf-8'), account.get_password()):
                label.configure(text="Login successful")
                self.user_screen(account)
            else:
                label.configure(text="Login failed. Please try again.")

        else:
            label.configure(text="Login failed. Please try again.")

    '''
    USER SCREEN SECTION
    '''
    # User "home page"
    def user_screen(self, account):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("green")

        self.current_frame.destroy()
        frame = ctk.CTkFrame(master=self.root)
        frame.pack(pady=20, padx=60, fill="both", expand=True)
        self.current_frame = frame
        label = ctk.CTkLabel(master=frame, text="Select an option")
        label.pack(pady=12, padx=10)

        # 1) Display all user information
        button = ctk.CTkButton(master=frame, text="Display all user information", command=lambda: self.display_user_info(account))
        button.pack(pady=12, padx=10)

        # 2) Edit user profile
        button = ctk.CTkButton(master=frame, text="Edit user profile", command=lambda: self.edit_profile(account))
        button.pack(pady=12, padx=10)

        # 3) Generate income tax estimate
        button = ctk.CTkButton(master=frame, text="Generate income tax estimate", command=lambda: self.generate_estimate(account))
        button.pack(pady=12, padx=10)

        # 4) Exit
        button = ctk.CTkButton(master=frame, text="Exit", command=lambda: self.root.destroy())
        button.pack(pady=12, padx=10)

        self.root.mainloop()

    # 1) Display all user information
    def display_user_info(self, account):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("green")

        self.current_frame.destroy()
        frame = ctk.CTkFrame(master=self.root)
        frame.pack(pady=20, padx=60, fill="both", expand=True)
        self.current_frame = frame
        label = ctk.CTkLabel(master=frame, text="User Info")
        label.pack(pady=12, padx=10)

        # Fill this in with displayed user info


        button = ctk.CTkButton(master=frame, text="Return", command=lambda: self.user_screen(account))
        button.pack(pady=12, padx=10)

        self.root.mainloop()

    # 2) Edit user profile
    def edit_profile(self, account):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("green")

        self.current_frame.destroy()
        frame = ctk.CTkFrame(master=self.root)
        frame.pack(pady=20, padx=60, fill="both", expand=True)
        self.current_frame = frame
        label = ctk.CTkLabel(master=frame, text="Edit Profile")
        label.pack(pady=12, padx=10)

        # Fill this in with edit profile functionality


        button = ctk.CTkButton(master=frame, text="Return", command=lambda: self.user_screen(account))
        button.pack(pady=12, padx=10)

        self.root.mainloop()

    # 3) Generate income tax estimate
    def generate_estimate(self, account):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("green")

        self.current_frame.destroy()
        frame = ctk.CTkFrame(master=self.root)
        frame.pack(pady=20, padx=60, fill="both", expand=True)
        self.current_frame = frame
        label = ctk.CTkLabel(master=frame, text="Generate Estimate")
        label.pack(pady=12, padx=10)

        # Fill this in with generate estimate functionality


        button = ctk.CTkButton(master=frame, text="Return", command=lambda: self.user_screen(account))
        button.pack(pady=12, padx=10)

        self.root.mainloop()

    '''
    ADMIN SCREEN SECTION
    '''
    # Admin "home page"
    def admin_screen(self, account):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("green")

        self.current_frame.destroy()
        frame = ctk.CTkFrame(master=self.root)
        frame.pack(pady=20, padx=60, fill="both", expand=True)
        self.current_frame = frame
        label = ctk.CTkLabel(master=frame, text="Select an option")
        label.pack(pady=12, padx=10)

        # 1) Display all user data
        button = ctk.CTkButton(master=frame, text="Display all user data", command=lambda: self.display_user_data(account))
        button.pack(pady=12, padx=10)

        # 2) Display user information by username
        button = ctk.CTkButton(master=frame, text="Edit user profile", command=lambda: self.display_user_by_name(account))
        button.pack(pady=12, padx=10)

        # 3) Delete user by user name
        button = ctk.CTkButton(master=frame, text="Generate income tax estimate", command=lambda: self.delete_user(account))
        button.pack(pady=12, padx=10)

        # 4) Display tax table
        button = ctk.CTkButton(master=frame, text="Display tax table", command=lambda: self.display_tax_table(account))
        button.pack(pady=12, padx=10)

        # 5) Exit
        button = ctk.CTkButton(master=frame, text="Exit", command=lambda: self.root.destroy())
        button.pack(pady=12, padx=10)

        self.root.mainloop()

    # 1) Display all user data
    def display_user_data(self, account):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("green")

        self.current_frame.destroy()
        frame = ctk.CTkFrame(master=self.root)
        frame.pack(pady=20, padx=60, fill="both", expand=True)
        self.current_frame = frame
        label = ctk.CTkLabel(master=frame, text="User Info")
        label.pack(pady=12, padx=10)

        # Fill this in with displayed user info


        button = ctk.CTkButton(master=frame, text="Return", command=lambda: self.admin_screen(account))
        button.pack(pady=12, padx=10)

        self.root.mainloop()

    # 2) Display user information by username
    def display_user_by_name(self, account):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("green")

        self.current_frame.destroy()
        frame = ctk.CTkFrame(master=self.root)
        frame.pack(pady=20, padx=60, fill="both", expand=True)
        self.current_frame = frame
        label = ctk.CTkLabel(master=frame, text="User Info")
        label.pack(pady=12, padx=10)

        # Fill this in with displayed user info


        button = ctk.CTkButton(master=frame, text="Return", command=lambda: self.admin_screen(account))
        button.pack(pady=12, padx=10)

        self.root.mainloop()

    # 3) Delete user by user name
    def delete_user(self, account):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("green")

        self.current_frame.destroy()
        frame = ctk.CTkFrame(master=self.root)
        frame.pack(pady=20, padx=60, fill="both", expand=True)
        self.current_frame = frame
        label = ctk.CTkLabel(master=frame, text="User Info")
        label.pack(pady=12, padx=10)

        # Fill this in with delete user logic


        button = ctk.CTkButton(master=frame, text="Return", command=lambda: self.admin_screen(account))
        button.pack(pady=12, padx=10)

        self.root.mainloop()

    # 4) Display tax table
    def display_tax_table(self, account):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("green")

        self.current_frame.destroy()
        frame = ctk.CTkFrame(master=self.root)
        frame.pack(pady=20, padx=60, fill="both", expand=True)
        self.current_frame = frame
        label = ctk.CTkLabel(master=frame, text="User Info")
        label.pack(pady=12, padx=10)

        # Fill this in with displayed tax table


        button = ctk.CTkButton(master=frame, text="Return", command=lambda: self.admin_screen(account))
        button.pack(pady=12, padx=10)

        self.root.mainloop()

    # ** FROM HERE DOWN IS DEPRECATED AND DOES NOT DO ANYTHING IN THE GUI IMPLEMENTATION, IT ONLY EXISTS AS REFERENCE FOR IMPLEMENTING THE GUI
        
    # Displays the interface for a signed-in user of non-admin account
    def display_user_interface(self):
        print("\nWelcome to Shuttle Cash!")
        print("1) Display all user information")
        print("2) Edit user profile")
        print("3) Generate income tax estimate")
        print("4) Exit\n")
        choice = input("Please enter your choice: ")
        return choice
    
    # Handles functionality for the interface for a signed-in user of non-admin account
    def manage_user_interface(self, account):
        choice = 0
        while choice != 4:
            choice = self.display_user_interface()
            match choice:
                # 1) Display all user information
                case "1":
                    account.display_user_info()
                    account_records = tax_table_manager.get_tax_records(account.get_user_name())
                    for record in account_records:
                        record.display_tax_info()
                # 2) Edit user profile
                case "2":
                    while True:
                        print("\nSelect an attribute to edit:")
                        print("1. Password")
                        print("2. Email")
                        print("3. First Name")
                        print("4. Last Name")
                        print("5. Submit changes")
                        choice = input("Enter your choice: \n")

                        if choice == "1":
                            hashed_password = bcrypt.hashpw(validate_password().encode('utf-8'), bcrypt.gensalt())
                            account.set_password(hashed_password)
                        elif choice == "2":
                            account.set_email(validate_email())
                        elif choice == "3":

                            account.set_first_name(validate_first_name())
                        elif choice == "4":
                            account.set_last_name(validate_last_name())

                        elif choice == "5":
                            user_table_manager.update_user(account)
                            break
                        else:
                            print("Invalid choice. Please enter a number between 1 and 5.")
                # 3) Generate income tax estimate
                case "3":
                    year = validate_year(account.get_user_name())
                    status = validate_status()
                    total_income = validate_total_income()
                    new_record = TaxRecord(account.get_user_name(), year, status, total_income)

                    tax_table_manager.add_tax_info(new_record)
                # 4) Exit
                case "4":
                    break
                # Default value
                case _:
                    print("\nCHOICE NOT IN SELECTION")
    
    def new_account(self, user_table_manager):
        while True:
            user_name = validate_user_name()
            password = validate_password()

            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

            email = validate_email()
            first_name = validate_first_name()
            last_name = validate_last_name()
            user = Account(user_name, hashed_password, email, first_name, last_name)

            if user_table_manager.add_user(user):
                return user


    # Displays the interface for a signed-in user of admin type
    def display_admin_interface(self):
        print("\nWelcome to Shuttle Cash!")
        print("ADMIN OPTIONS")
        print("1) Display all user data")
        print("2) Display user information by user name")
        print("3) Delete user by user name")
        print("4) Display tax table")
        print("5) Exit")
        choice = input("Please enter your choice: ")

        return choice

    # Handles the functionality for the interface for a signed-in user of admin type
    def manage_admin_interface(self):
        choice = 0
        while choice != "5":
            choice = self.display_admin_interface()
            match choice:
                # 1) Display all user data
                case "1":
                    user_table_manager.display_table()
                    tax_table_manager.display_table()
                # 2) Display user information by username
                case "2":
                    user_name = validate_user_name()
                    if user_table_manager.get_account_by_user_name(user_name):
                        account = user_table_manager.get_account_by_user_name(user_name)
                        account.display_user_info()
                        account_records = tax_table_manager.get_tax_records(user_name)
                        for record in account_records:
                            record.display_tax_info()
                    else:
                        print("Error: Unable to find a matching username.")

                # 3) Delete user by user name
                case "3":
                    user_name = validate_user_name()
                    user_table_manager.delete_user(user_name)
                    # tax_table_manager.delete_user(user_id)
                # 4) Display tax table
                case "4":
                    tax_table_manager.display_table()
                # 5) Exit
                case "5":
                    break
                # Default value
                case _:
                    print("\nCHOICE NOT IN SELECTION")
