from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app import mysql, mail
from flask_mail import Message
import hashlib, random

auth = Blueprint('auth', __name__)

@auth.route('/')
def index():
    return render_template('index.html')

@auth.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = hashlib.sha256(request.form['password'].encode()).hexdigest()
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE username=%s AND password=%s AND Status='active'", (username,password))
        user = cur.fetchone()
        cur.close()
        if user:
            session['loggedin'] = True
            session['user_id'] = user[0]
            session['username'] = user[8]
            session['role'] = user[10]
            if user[10] == 'admin':
                return redirect(url_for('dashboard.admin_dashboard'))
            return redirect(url_for('dashboard.user_dashboard'))
        else:
            flash("Invalid credentials or inactive account!")
    return render_template('login.html')

@auth.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))

@auth.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = hashlib.sha256(request.form['password'].encode()).hexdigest()
        otp = random.randint(100000, 999999)
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users (username,email,password,Status) VALUES (%s,%s,%s,'inactive')",
                    (username,email,password))
        mysql.connection.commit()
        cur.close()
        msg = Message("OTP Verification", sender="your_email@gmail.com", recipients=[email])
        msg.body = f"Your OTP is: {otp}"
        mail.send(msg)
        session['otp'] = otp
        session['email'] = email
        flash("OTP sent to your email.")
        return redirect(url_for('auth.verify_otp'))
    return render_template('register.html')

@auth.route('/verify_otp', methods=['GET','POST'])
def verify_otp():
    if request.method == 'POST':
        entered_otp = request.form['otp']
        if int(entered_otp) == session.get('otp'):
            cur = mysql.connection.cursor()
            cur.execute("UPDATE users SET Status='active' WHERE email=%s", (session['email'],))
            mysql.connection.commit()
            cur.close()
            flash("Account verified successfully!")
            return redirect(url_for('auth.login'))
        else:
            flash("Incorrect OTP.")
    return render_template('verify_otp.html')
