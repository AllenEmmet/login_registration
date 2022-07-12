from flask_app.config.mysqlconnections import connectToMySQL
import re	# the regex module
# create a regular expression object that we'll use later   
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from flask import flash



class User:
    db = "login_reg"
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        responses = connectToMySQL(cls.db).query_db(query)
        users = []
        for row in responses:
            users.append(cls(row))
        return users

    @classmethod
    def get_one_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        responses = connectToMySQL(cls.db).query_db(query, data)
        if len(responses) < 1:
            return False
        return cls(responses[0])

    @classmethod
    def get_one_id(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        responses = connectToMySQL(cls.db).query_db(query, data)
        return cls(responses[0])

    @staticmethod
    def validate_registration(user):
        is_valid = True
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(User.db).query_db(query, user)
    
        if len(results) >= 1:
            flash("Email already taken", "registration")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash("wrong email!", "registration")
            is_valid = False
        if user['password'] != user['confirm_password']:
            flash("Passwords do not match", "registration")
            is_valid = False
        print('validate working')
        return is_valid


  

