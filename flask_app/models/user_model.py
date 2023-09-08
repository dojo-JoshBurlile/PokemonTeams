from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app import bcrypt
import re

db = "pokemon_teams_schema"
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
class User:
    def __init__(self, db_data):
        self.id = db_data['id']
        self.email = db_data['email']
        self.username = db_data['username']
        self.password = db_data['password']
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']


    @classmethod
    def save_user(cls, form_data):
        hashed_data = {
            'email': form_data['email'],
            'username': form_data['username'],
            'password': bcrypt.generate_password_hash(form_data['password']),
        }
        query = """
                INSERT INTO users (email, username, password) VALUES (%(email)s, %(username)s, %(password)s)
                """
        return connectToMySQL(db).query_db(query, hashed_data)
    
    @classmethod
    def get_by_email(cls, data):
        query = """
                SELECT * FROM users WHERE email = %(email)s;
                """
        result = connectToMySQL(db).query_db(query, data)
        if not result:
            return False
        
        return cls(result[0])
    
    @staticmethod
    def validate_login(form_data):
        if not EMAIL_REGEX.match(form_data['email']):
            flash("Invalid email/password", "login")
            return False
        user = User.get_by_email(form_data)
        if not user:
            flash("Invalid email/password", "login")
            return False
        if not bcrypt.check_password_hash(user.password, form_data['password']):
            flash("Invalid email/password", "login")
            return False
        
        return user
    
    @staticmethod
    def validate_reg(form_data):
        is_valid = True

        if len(form_data['email']) < 1:
            flash("Email cannot be blank.","register")
            is_valid = False
        elif not EMAIL_REGEX.match(form_data['email']):
            flash("Invalid email address.","register")
            is_valid = False
        elif User.get_by_email(form_data):
            flash("A user already exists for that email.","register")
            is_valid = False
        if len(form_data['password']) < 8:
            flash("Password must be at least 8 characters long.","register")
            is_valid = False
        if form_data['password'] != form_data['confirm_password']:
            flash("Passwords must match.","register")
            is_valid = False
        if len(form_data['username']) >= 15:
            flash("Username must be less than 15 characters long.","register")
            is_valid = False

        return is_valid

