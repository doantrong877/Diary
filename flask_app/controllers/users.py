from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.post import Post
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

#load home page
@app.route('/')
def home():
    return render_template('home.html')

#load register page
@app.route('/register')
def register():
    return render_template('register.html')

#register route
@app.route('/registerform', methods=['POST'])
def registerform():

    #check for invalid input
    if not User.validate_registration(request.form):
        return redirect('/register')
    
    
    #check matching password
    if request.form['password'] != request.form['confirm_password']:
        flash("Passwords must match", 'register')
        return redirect('/register')

    #hash password
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    
    #put hash password into data
    data = {
        "first_name" : request.form['first_name'],
        "last_name" : request.form['last_name'],
        "email" : request.form['email'],
        "password" : pw_hash
    }
    #assign session id
    session['user_id'] = User.save(data)
    return redirect('/dashboard')

#signin
@app.route('/login')
def login():
    return render_template('login.html')


#login route
@app.route('/loginform', methods=['POST'])
def loginform():
    
    #check if there is email in db
    data_email = {
        'email' : request.form['email']
    }
    user = User.get_by_email(data_email)
    if not user :
        flash('Invalid Email/Password', 'login')
        return redirect('/login')
    
    #check if password match db pass
    if not bcrypt.check_password_hash(user.password,request.form['password']):
        flash('Invalid Email/Password','login')
        return redirect('/login')
    session['user_id'] = user.id
    return redirect('/dashboard')

#Welcome page
@app.route('/dashboard')
def dashboard():
    data ={
        'id' : session['user_id']
    }
    return render_template('dashboard.html', name = f"{User.get_one(data).first_name} {User.get_one(data).last_name}", posts = User.get_user_with_posts())

#logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')