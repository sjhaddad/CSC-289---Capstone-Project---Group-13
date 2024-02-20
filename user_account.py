from constants import *


# from user_table_manager import User_table_manager


class UserAccount:

    def __init__(self, user_name, password, email, first_name, last_name):
        self.user_name = user_name
        self.password = password
        self.email = email
        self.first_name = first_name
        self.last_name = last_name

        # self.user_table_manager = User_table_manager
        # Getter methods

    def get_user_name(self):
        return self.user_name

    def get_password(self):
        return self.password

    def get_email(self):
        return self.email

    def get_first_name(self):
        return self.first_name

    def get_last_name(self):
        return self.last_name

        # Setter methods

    def set_user_name(self, user_name):
        self.user_name = user_name

    def set_password(self, password):
        self.password = password

    def set_email(self, email):
        self.email = email

    def set_first_name(self, first_name):
        self.first_name = first_name

    def set_last_name(self, last_name):
        self.last_name = last_name

    def display_user_info(self):
        print( f'\nUser Name: {UserAccount.get_user_name(self)}\nPassword: {UserAccount.get_password(self)}\n' \
               f'Email: {UserAccount.get_email(self)}\nFirst Name: {UserAccount.get_first_name(self)}\nLast Name: {UserAccount.get_last_name(self)}\n')
