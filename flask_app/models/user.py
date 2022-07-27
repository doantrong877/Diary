from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app import app
import re
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users"
        results = connectToMySQL('blogs_schema').query_db(query)
        users = []
        for user in results:
            users.append(cls(user))
        return users
    
    @classmethod
    def save(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password, created_at, updated_at) VALUES (%(first_name)s,%(last_name)s,%(email)s,%(password)s,NOW(),NOW());"
        return connectToMySQL('blogs_schema').query_db(query,data)

    @classmethod
    def get_one(cls,data):
        query = "SELECT * FROM users WHERE users.id = %(id)s;"
        result = connectToMySQL('blogs_schema').query_db(query,data)
        return cls(result[0])

    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE users.email = %(email)s;"
        result = connectToMySQL('blogs_schema').query_db(query,data)
        if len(result) < 1:
            return False
        return cls(result[0])

    @classmethod
    def get_user_with_posts(cls):
        query = "SELECT *,posts.id as post_id, posts.created_at as date FROM users LEFT JOIN posts ON users.id = posts.user_id;"
        result = connectToMySQL('blogs_schema').query_db(query)
        users = []

        for user in result:
            users.append(user)
        return users

    @classmethod
    def validate_registration(cls, data):
        is_valid = True

        if len(data['first_name']) < 2:
            flash("First name has two have at least 2 character",'register')
            is_valid = False
        if len(data['last_name']) < 2:
            flash("Last name has two have at least 2 character",'register')
            is_valid = False
        if not EMAIL_REGEX.match(data['email']):
            flash("Invalid email addess!",'register')
            is_valid = False
        if len(data['password']) < 8:
            flash("Password has two have at least 8 character",'register')
            is_valid = False
        query = "SELECT * FROM users;"
        results = connectToMySQL('blogs_schema').query_db(query)
        for email_info in results:
            if cls(email_info).email == data['email']:
                flash("email has already registed",'register')
                is_valid = False
        return is_valid


    
    