#from faker import Faker
import os
import time
import random
import sqlite3
from datetime import datetime, timedelta
from flask import Flask, render_template, request, url_for, flash, redirect, session
from flask_session import Session
from werkzeug.exceptions import abort
from waitress import serve
from dateutil import parser

#from flask_login import login_user, login_required, \
    #logout_user, current_user, LoginManager
#from flask_login import UserMixin
#import init_db

#fake = Faker() ## use for 10Analytics project


# create a database connection and return it
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# validate and get post
def get_post(access_code):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE access_code = ?', \
                       (access_code,)).fetchone()
    conn.close()
    # validate: if no entry in db, respond with 404 error code.
    if post is None:
        abort(404)
    # if post was found in db, return the value of the post.
    return post

# validate and get user
def get_user(user_id):
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE user_id = ?', \
                       (user_id,)).fetchone()
    conn.close()
    # validate: if no entry in db, respond with 404 error code.
    if user is None:
        abort(404)
    # if post was found in db, return the value of the post.
    return user

def get_admin(admin_id):
    conn = get_db_connection()
    admin = conn.execute('SELECT * FROM admin_users WHERE admin_id = ?', \
                       (admin_id,)).fetchone()
    conn.close()
    # validate: if no entry in db, respond with 404 error code.
    if admin is None:
        abort(404)
    # if post was found in db, return the value of the post.
    return admin

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
# The 'SECRET_KEY' can be your password
SECRET_KEY = os.getenv('SECRET_KEY')
app.config['SECRET_KEY'] = SECRET_KEY
#db = sqlite3


# View the starting page
@app.route('/')
def home():
    users = [
        url_for('login'),
        url_for('validate'), 
        url_for('admin_login')
    ]    
    if users.count == 3:
        breakpoint
        
    return render_template('home.html', users=users)

# View all in the database via the index page
@app.route('/index')
def index():
    if request.method == 'GET':
        if session.get('user') == None:
            if session.get('user_name'):
                flash('Please Login', category='error')
            return redirect(url_for('admin_login'))
    # open a database connection. 
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts').fetchall()
    conn.close()
    return render_template('index.html', posts=posts)

@app.route('/users')
# View all registered users in the database via the users page
def users():
    if request.method == 'GET':
        if session.get('user') == None:
            if session.get('user_name'):
                flash('Please Login', category='error')
            return redirect(url_for('admin_login'))
    # open a database connection. 
    conn = get_db_connection()
    users = conn.execute('SELECT * FROM users').fetchall()
    conn.close()
    return render_template('users.html', users=users)

# view function to receive an integer after '/'
@app.route('/<int:access_code>')
def post(access_code):
    # get the details from the db with the given post_id
    post = get_post(access_code)
    # pass the details of post to the post.html page for display 
    return render_template('post.html', post=post)

# view function to receive an integer after '/'
@app.route('/<int:user_id>/user')
def view(user_id):
    # get the details from the db with the given user_id
    user = get_user(user_id)
    # pass the details of user to the users.html page for display 
    return render_template('view.html', user=user)

# a view function to login users
@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        session["user_name"] = request.form["user_name"]
        password = request.form['user_psswrd']
        c = datetime.now()
        current_time = c.strftime('%Y-%m-%d')
        # Pass the 'user_name' stored in session to the variable 'u_name' 
        u_name = session.get('user_name')
        # flash a message if 'username' or 'password' is omitted 
        if not u_name:
            flash('username is required', category='error')
        elif not password:
            flash('Enter a password', category='error')
        # Insert a username and password into the db
        else:
            conn = get_db_connection()
            user = conn.execute('SELECT * FROM users WHERE email = ?', \
                                (u_name,)).fetchone()
            login_user = conn.execute('SELECT * FROM user_login WHERE user_name = ?', \
                                    (u_name,)).fetchone()
            # if user is not registered, display a flash message
            validity_date = user['validity_date']
            formatted_val_date = parser.parse(validity_date).strftime('%Y-%m-%d')
            if not user:
                flash("Please contact the Office Admin", category='error')
            # check validity and delete from database if expired.
            elif current_time > formatted_val_date:#user['validity_date']:
                flash('Validity expired! Please contact office admin', category='error')
                conn.execute('DELETE FROM users WHERE email = ?', (u_name, ))
                conn.execute('DELETE FROM user_login WHERE user_name = ?', (u_name, ))
                conn.commit()
            # if user exists, store login details in the database. 
            elif not login_user:
                if user['email'] == u_name:
                    conn.execute('INSERT INTO user_login (user_name, user_psswrd) VALUES (?, ?)', \
                                (u_name, password))
                    conn.commit()
                    conn.close()

                    #id = user['user_id']
                    a = session["user_name"]
                    
                    return redirect(url_for('create'))
            
            elif login_user['user_psswrd'] == password and login_user['user_name'] == u_name:
                flash('Login successful!', category='success')
                
                return redirect(url_for('create'))
            else:
                flash('Wrong username or password', category='error')  
    #validate_url()          
    return render_template('login.html')

@app.route('/logout')
#@login_required
def logout():
    session['user_name'] = None
    return redirect(url_for('login'))


# a view function to create/generate posts/access codes
@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        # Confirm if user was logged in
        a = session.get('user_name') 
        if not a:
            return redirect(url_for('login'))
        else:
            guest_name = request.form['guest_name']
            host_address = request.form['host_address']
        # flash a message if 'Name' or 'Address' is omitted 
            if not guest_name:
                flash('Name is required', category='error')
            elif not host_address:
                flash('Address is required', category='error')
        # Enter Name, Address and access code into the db
            else:
            # Generate the 5-digit Access code
                access_code = f'{random.randint(10000, 99999)}'
                expired = (datetime.now() + timedelta(hours=0)).strftime('%Y-%m-%d %H:%M:%S')
                conn = get_db_connection()
                conn.execute('INSERT INTO posts (guest_name, host_address, access_code, expired) VALUES (?, ?, ?, ?)',\
                            (guest_name, host_address, access_code, expired))
                conn.commit()
                conn.close()
                return redirect(url_for('post_edit', id=access_code))
    # enforce login: can't get to the url without 1st loggin in.
    elif request.method == 'GET':
        if not session.get('user_name'):
            flash('Please Login', category='error')
            return redirect(url_for('login'))    
    
    return render_template('create.html')

# use this view function to edit the guest name and host address
@app.route('/<int:id>/edit', methods=('GET', 'POST'))
def edit(id):
    post = get_post(id)

    if request.method == 'POST':
        guest_name = request.form['guest_name']
        host_address = request.form['host_address']

        if not guest_name:
            flash('Name is required', category='error')
        else:
            conn = get_db_connection()
            conn.execute('UPDATE posts SET guest_name = ?, host_address = ?'
                         'WHERE id = ?',
                         (guest_name, host_address, id))
            conn.commit()
            conn.close()
            return redirect(url_for('post_edit', id=id))
    # enforce login: can't get to the url without 1st loggin in.
    elif request.method == 'GET':
        if not session.get('user_name'):
            flash('Please Login', category='error')
            return redirect(url_for('login'))        
    
    return render_template('edit.html', post=post)

# use this view function to edit the guest name and host address

@app.route('/<int:id>/post_edit')
def post_edit(id):
    # get the details from the db with the given post_id
    post = get_post(id)
    # pass the details of post to the post.html page for display 
    return render_template('post_edit.html', post=post)
        

# use this view function to edit the guest name and host address

@app.route('/<int:user_id>/user_edit', methods=('GET', 'POST'))
def user_edit(user_id):
    user = get_user(user_id)

    if request.method == 'POST':
        full_name = request.form['full_name']
        resident_address = request.form['resident_address']
        email = request.form['email']

        if not full_name:
            flash('Name is required', category='error')
        else:
            conn = get_db_connection()
            conn.execute('UPDATE users SET full_name = ?, resident_address = ?, email = ?'
                         'WHERE user_id = ?',
                         (full_name, resident_address, email, user_id))
            conn.commit()
            conn.close()
            return redirect(url_for('users'))

    # enforce login: can't get to the url without 1st loggin in.
    elif request.method == 'GET':
        if not session.get('user_name'): # for admin users
            flash('Please Login', category='error')
            return redirect(url_for('login'))        

    return render_template('user_edit.html', user=user)

# a view function to validate access codes
@app.route('/validate', methods=('GET', 'POST'))
def validate():
    if request.method == 'POST':
        access_code = request.form['access_code']
        # flash a message if 'Name' or 'Address' is omitted
        a = datetime.now()
        a_time = a.strftime('%Y-%m-%d %H:%M:%S') 
        if not access_code:
            flash('Access code is required', category='error')
        # Fetch Name, Address and access code from the db
        else:
            conn = get_db_connection()
            post = get_post(access_code)
            e_time = post['expired']          
            if a_time >= e_time:
                flash('Access code is validated', category= 'success')  
                conn.execute('DELETE FROM posts WHERE access_code = ?', (access_code, ))
                conn.commit()
                conn.close()
            else:
                return redirect(url_for('post', access_code=access_code))
        
    return render_template('validate.html')

# a view function to register users
@app.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        name = request.form['full_name']
        resident_address = request.form['resident_address']
        email = request.form['email']
        validity = request.form['validity_date']
        # flash a message if 'Name' or 'Address' is omitted 
        if not name:
            flash('Name is required', category='error')
        elif not resident_address:
            flash('Address is required', category='error')
        elif not email:
            flash('email is required', category='error')
        elif not validity:
            flash('Validity date is required', category='error')
        # Enter Name, Address, email and validity date into the db
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO users (full_name, resident_address, email, validity_date) VALUES (?, ?, ?, ?)',
                         (name, resident_address, email, validity))
            conn.commit()
            conn.close()
            return redirect(url_for('users'))

    # enforce login: can't get to the url without 1st loggin in.
    elif request.method == 'GET':
        if not session.get('user'): # for admin users
            flash('Please Login', category='error')
            return redirect(url_for('admin_login'))        

    return render_template('register.html')

# a view function to LOGIN admin users.
@app.route('/admin_login', methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        session["user"] = request.form["username"]
        password = request.form['admin_psswrd']
        c = datetime.now()
        current_time = c.strftime('%Y-%m-%d')
        # Pass the 'user_name' stored in session to the variable 'u_name' 
        a_name = session.get('user')
        # flash a message if 'username' or 'password' is omitted 
        if not a_name:
            flash('username is required', category='error')
        elif not password:
            flash('Enter a password', category='error')
        # Insert a username and password into the db
        else:
            conn = get_db_connection()
            admin = conn.execute('SELECT * FROM admin_users WHERE email = ?', \
                                (a_name,)).fetchone()
            login_admin = conn.execute('SELECT * FROM a_login WHERE username = ?', \
                                    (a_name,)).fetchone()
            a_val_date = admin['validity_date']
            formatted_a_val_date = parser.parse(a_val_date).strftime('%Y-%m-%d') # format admin validity date
            # if user is not registered, display a flash message
            if not admin:
                flash("You are not a registered admin. Please contact the RVE EXCO", category='error')
            # check validity and delete from database if expired.
            elif current_time > formatted_a_val_date: #admin['validity_date']:
                flash('Validity expired! Please contact office admin', category='error')
                conn.execute('DELETE FROM admin_users WHERE email = ?', (a_name, ))
                conn.execute('DELETE FROM a_login WHERE username = ?', (a_name, ))
                conn.commit()
            # if admin exists, store login details in the database. 
            elif not login_admin:
                if admin['email'] == a_name:
                    conn.execute('INSERT INTO a_login (username, admin_psswrd) VALUES (?, ?)', \
                                (a_name, password))
                    conn.commit()
                    conn.close()

                    #id = user['user_id']
                    #a = session["user_name"]
                    
                    return redirect(url_for('users'))
            
            elif login_admin['admin_psswrd'] == password and login_admin['username'] == a_name:
                flash('Login successful!', category='success')
                if admin['a_profile'] == 'super admin':
                    return redirect(url_for('admin_signup'))
                else:
                    return redirect(url_for('register'))
            else:
                flash('Wrong username or password', category='error')  
    #validate_url()          
    return render_template('admin_login.html')

# Logout admin users.
@app.route('/alogout')
#@login_required
def alogout():
    session['user'] = None
    #session['profile'] = None
    return redirect(url_for('admin_login'))


# a view function to register admin users
@app.route('/admin_signup', methods=('GET', 'POST'))
def admin_signup():
    if request.method == 'POST':
        name = request.form['full_name']
        address = request.form['address']
        session['user_name'] = request.form['email']
        profile = request.form['profile']
        validity = request.form['validity_date']
        
        email = session.get('user_name')
        #profile = session.get('profile')

        # flash a message if 'Name' or 'Address' is omitted 
        if not name:
            flash('Name is required', category='error')
        elif not address:
            flash('Address is required', category='error')
        elif not email:
            flash('email is required', category='error')
        elif not profile:
            flash('Profile is required', category='error')
        elif not validity:
            flash('Validity date is required', category='error')
        # Enter Name, Address, email, profile and validity date into the db
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO admin_users (full_name, a_address, email, validity_date, a_profile) VALUES (?, ?, ?, ?, ?)',
                         (name, address, email, profile, validity))
            conn.commit()
            conn.close()
            return redirect(url_for('admin_users'))

    # enforce login: can't get to the url without 1st loggin in.
    elif request.method == 'GET':
        if session.get('user') == None: # for admin users
            if session.get('user_name'):
                flash('Please Login', category='error')
            return redirect(url_for('admin_login'))        

    return render_template('admin_signup.html')

@app.route('/admin_users')
# View all registered admin users in the database.
def admin_users():
    if request.method == 'GET':
        if session.get('user') == None:
            if session.get('user_name'):
                flash('Please Login', category='error')
            return redirect(url_for('admin_login'))
    # open a database connection. 
    conn = get_db_connection()
    admin_users = conn.execute('SELECT * FROM admin_users').fetchall()
    conn.close()
    return render_template('admin_users.html', admin_users=admin_users)


# view function to receive an integer after '/'
@app.route('/<int:admin_id>/view_admin')
def view_admin(admin_id):
    # get the details from the db with the given user_id
    admin = get_admin(admin_id)
    # pass the details of user to the users.html page for display 
    return render_template('view_admin.html', user=admin)


@app.route('/reset', methods=('POST', 'GET'))
def reset():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        # check if username and password is entered
        if not username:
            flash('Please enter a valid username', category='error')
        elif not password:
            flash('Please enter a password', category='error')
        elif not email:
            flash('please enter a valid email', category='error')
    #post = get_post(id)
        else:
            conn = get_db_connection()
            reset = conn.execute('SELECT * FROM user_login WHERE user_name = ?', (username,)).fetchone()
            a_reset = conn.execute('SELECT * FROM a_login WHERE username = ?', (username,)).fetchone()
            sa = conn.execute('SELECT admin_psswrd FROM a_login WHERE admin_psswrd = ?', (password,)).fetchone()
            # check if username is correct/registered and if password matches super admin profile
            if sa:           
                if reset:
                    conn.execute('DELETE FROM user_login WHERE user_name = ?', (username,))
                    conn.commit()
                    conn.close()
                    flash('"{}" was successfully deleted!'.format(reset['user_name']))
                elif a_reset:
                    conn.execute('DELETE FROM a_login WHERE username = ?', (username,))
                    conn.commit()
                    conn.close()
                    flash('"{}" was successfully deleted!'.format(a_reset['username']))
                else:
                    flash('Wrong username or not registered!', category='error')
            else:
                flash('You are not authorized!', category='error')
            
            alogout()
            return redirect(url_for('admin_login'))
    
    elif request.method == 'GET':
        if session.get('user') == None:
            if session.get('user_name'):
                flash('You are not authorized!', category='error')
            return redirect(url_for('home'))
        
    return render_template('reset.html')


@app.route('/<int:id>/delete', methods=('POST', 'GET'))
def delete(id):
    post = get_post(id)
    if post:
        conn = get_db_connection()
        conn.execute('DELETE FROM posts WHERE access_code = ?', (id,))
        conn.commit()
        conn.close()
        flash('"{}" was successfully deleted!'.format(post['guest_name']))
        return redirect(url_for('logout'))
    else:
        flash('no records found', category='error')
        return redirect(url_for('create'))

    return render_template('delete.html', post=post)


if __name__ == '__main__':
    serve(app, host="0.0.0.0", port=5050)
    #app.run(debug=True, port=5050) # for testing/demo
