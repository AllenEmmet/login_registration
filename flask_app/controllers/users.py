from flask import render_template, redirect, request, session, flash

from flask_app import app

from flask_app.models.user import User

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def route():
    return render_template ('index.html')

@app.route('/register', methods=["POST"])
def register():
    if not User.validate_registration(request.form):
        return redirect('/')
    data = {
        "first_name" : request.form['first_name'],
        "last_name" : request.form['last_name'],
        "email" : request.form['email'], 
        "password" : bcrypt.generate_password_hash(request.form['password'])



    }
    session['user'] = User.save(data)
    print('register working')
    return redirect('/welcome')

@app.route('/login', methods=["POST"])
def login():
    user = User.get_one_email(request.form)
    if not user:
        flash("Invalid Email", "login")
        return redirect('/')
    
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Invalid Password", "login")
        return redirect('/')
    session['user'] = user.id
    return redirect('/welcome')
    

@app.route('/welcome')
def welcome():
    if 'user' not in session:
        return redirect ('/')
    data = {
        'id': session['user']
    }
    return render_template('login.html', user = User.get_one_id(data))

@app.route('/exit')
def logout():
    session.clear()
    return redirect ('/')