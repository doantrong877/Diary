from tokenize import Double
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Post:
    def __init__(self, data):
        self.id = data['id']
        self.user_id = data['user_id']
        self.title = data['title']
        self.content = data['content']
        self.highlight = data['highlight']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM posts"
        results = connectToMySQL('blogs_schema').query_db(query)
        posts = []
        for post in results:
            posts.append(cls(post))
        return posts
    
    @classmethod
    def get_post_by_id(cls,data):
        query = "SELECT * FROM posts WHERE posts.id = %(id)s;"
        result = connectToMySQL('blogs_schema').query_db(query,data)
        return cls(result[0])

    @classmethod
    def save(cls,data):
        query = "INSERT INTO posts(user_id,content,highlight,created_at,updated_at) VALUES (%(user_id)s,%(content)s,%(highlight)s,NOW(),NOW());"
        return connectToMySQL('blogs_schema').query_db(query,data)

    @classmethod
    def validate_post(cls, data):
        is_valid = True
        if len(data['content']) < 10:
            flash("Content must be at least 10 characters", "post")
            is_valid = False   
        if len(data['highlight']) < 5:
            flash("Content must be at least 5 characters", "post")
            is_valid = False 
        return is_valid

    @classmethod
    def destroy(cls,data):
        query = "DELETE FROM posts WHERE posts.id = %(id)s;"
        return connectToMySQL('blogs_schema').query_db(query,data)

    @classmethod
    def update(cls,data):
        query = "UPDATE posts SET user_id = %(user_id)s, content = %(content)s, highlight = %(highlight)s WHERE posts.id = %(post_id)s;"
        return connectToMySQL('blogs_schema').query_db(query,data)
