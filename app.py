#from faker import Faker
import time
import random
import sqlite3
from datetime import datetime
from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort

#fake = Faker()

# create a database connection and return it
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# Generate the 5-digit Access code
#def generate_code(name):


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

app = Flask(__name__)
# The 'SECRET_KEY' can be your password
app.config['SECRET_KEY'] = 'your secret key'

@app.route('/')

# View all in the database via the index page
def index():
    # open a database connection. 
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts').fetchall()
    conn.close()
    return render_template('index.html', posts=posts)

@app.route('/users')
# View all registered users in the database via the users page
def users():
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
@app.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        user_name = request.form['user_name']
        password = request.form['user_psswrd']
        c = datetime.now()
        current_time = c.strftime('%Y-%m-%d')
        # flash a message if 'username' or 'password' is omitted 
        if not user_name:
            flash('username is required')
        elif not password:
            flash('Enter a password')
        # Insert a username and password into the db
        else:
            conn = get_db_connection()
            user = conn.execute('SELECT * FROM users WHERE email = ?', \
                                (user_name,)).fetchone()
            login_user = conn.execute('SELECT * FROM user_login WHERE user_name = ?', \
                                      (user_name,)).fetchone()
            if not user:
                flash("Please contact the Office Admin")
            elif current_time > user['validity_date']:
                flash('Validity expired! Please contact office admin')
            elif not login_user:
                if user['email'] == user_name:
                    conn.execute('INSERT INTO user_login (user_name, user_psswrd) VALUES (?, ?)', \
                                (user_name, password))
                    conn.commit()
                    conn.close()
                    return redirect(url_for('create'))
            elif login_user['user_psswrd'] == password and login_user['user_name'] == user_name:
                flash('Login successful!')
                return redirect(url_for('create'))
            else:
                flash('Wrong username or password')            
    return render_template('login.html')


# a view function to create/generate posts/access codes
@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        guest_name = request.form['guest_name']
        host_address = request.form['host_address']
        # flash a message if 'Name' or 'Address' is omitted 
        if not guest_name:
            flash('Name is required')
        elif not host_address:
            flash('Address is required')
        # Enter Name, Address and access code into the db
        else:
            # Generate the 5-digit Access code
            access_code = f'{random.randint(10000, 99999)}'
            expired = time.time() + 4
            conn = get_db_connection()
            conn.execute('INSERT INTO posts (guest_name, host_address, access_code, expired) VALUES (?, ?, ?, ?)',
                         (guest_name, host_address, access_code, expired))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))
        
    return render_template('create.html')

# use this view function to edit the guest name and host address
@app.route('/<int:id>/edit', methods=('GET', 'POST'))
def edit(id):
    post = get_post(id)

    if request.method == 'POST':
        guest_name = request.form['guest_name']
        host_address = request.form['host_address']

        if not guest_name:
            flash('Name is required')
        else:
            conn = get_db_connection()
            conn.execute('UPDATE posts SET guest_name = ?, host_address = ?'
                         'WHERE id = ?',
                         (guest_name, host_address, id))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))
        
    return render_template('edit.html', post=post)

# use this view function to edit the guest name and host address

@app.route('/<int:user_id>/user_edit', methods=('GET', 'POST'))
def user_edit(user_id):
    user = get_user(user_id)

    if request.method == 'POST':
        full_name = request.form['full_name']
        resident_address = request.form['resident_address']
        email = request.form['email']

        if not full_name:
            flash('Name is required')
        else:
            conn = get_db_connection()
            conn.execute('UPDATE users SET full_name = ?, resident_address = ?, email = ?'
                         'WHERE user_id = ?',
                         (full_name, resident_address, email, user_id))
            conn.commit()
            conn.close()
            return redirect(url_for('users'))
        
    return render_template('user_edit.html', user=user)

# a view function to validate access codes
@app.route('/validate', methods=('GET', 'POST'))
def validate():
    if request.method == 'POST':
        access_code = request.form['access_code']
        # flash a message if 'Name' or 'Address' is omitted 
        if not access_code:
            flash('Access code is required')
        # Fetch Name, Address and access code from the db
        else:
            conn = get_db_connection()
            post = get_post(access_code)
            conn.close()
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
            flash('Name is required')
        elif not resident_address:
            flash('Address is required')
        elif not email:
            flash('email is required')
        elif not validity:
            flash('Validity date is required')
        # Enter Name, Address, email and validity date into the db
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO users (full_name, resident_address, email, validity_date) VALUES (?, ?, ?, ?)',
                         (name, resident_address, email, validity))
            conn.commit()
            conn.close()
            return redirect(url_for('users'))
        
    return render_template('register.html')

@app.route('/<int:id>/delete', methods=('POST',))
def delete(access_code):
    post = get_post(access_code)
    conn = get_db_connection()
    conn.execute('DELETE FROM posts WHERE access_code = ?', (access_code,))
    conn.commit()
    conn.close()
    flash('"{}" was successfully deleted!'.format(post['guest_name']))
    return redirect(url_for('index'))
