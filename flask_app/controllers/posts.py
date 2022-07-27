from flask_app import app
from flask_app.models.post import Post
from flask_app.models.user import User
from flask import flash, render_template, session, redirect, request

#add post
@app.route('/dashboard/create')
def create():
    data ={
        'id' : session['user_id']
    }
    return render_template('create.html',name = f"{User.get_one(data).first_name} {User.get_one(data).last_name}")

#save post
@app.route('/create', methods = ['POST'])
def save():
    if not Post.validate_post(request.form):
        return redirect('/dashboard/create')
    data = {
        'user_id' : session['user_id'],
        'content': request.form['content'],
        'highlight': request.form['highlight']
    }
    post_id = Post.save(data)

    post_data = {
        "id" : session['user_id']
    }
    return redirect('/dashboard')

#get post info
@app.route('/dashboard/post/<int:id>')
def get_painting_info(id):
    user_data ={
        'id' : session['user_id']
    }
    post_data = {
        'id' : id
    }
    session['post_id'] = id
    post = Post.get_post_by_id(post_data)
    poster = {
        'id': post.user_id
    }
    return render_template('view.html', name =f"{User.get_one(user_data).first_name} {User.get_one(user_data).last_name}" ,post = post)

#delete post
@app.route('/delete/<int:id>')
def delete_painting(id):
    data = {
        'id' : id
    }
    Post.destroy(data)
    return redirect('/dashboard')

#edit post
@app.route('/dashboard/edit/<int:id>')
def edit_painting(id):
    post_data = {
        'id' : id
    }
    user_data ={
        'id' : session['user_id']
    }
    post = Post.get_post_by_id(post_data)
    session['post_id'] = id
    return render_template('edit.html', post = post,name =f"{User.get_one(user_data).first_name} {User.get_one(user_data).last_name}")

#get data from edit
@app.route('/edit/post', methods=['POST'])
def edit():
    id = session['post_id']
    if not Post.validate_post(request.form):
        return redirect(f'/dashboard/edit/{id}')
    data = {
        'user_id' : session['user_id'],
        'highlight': request.form['highlight'],
        'content': request.form['content'],
        'post_id' : id
    }
    Post.update(data)
    return redirect('/dashboard')


