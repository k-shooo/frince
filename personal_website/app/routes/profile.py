from flask import Blueprint, render_template, session, request, redirect, url_for, flash
from app import mysql

profile = Blueprint('profile', __name__)

@profile.route('/profile', methods=['GET','POST'])
def profile_page():
    if 'loggedin' not in session:
        return redirect(url_for('auth.login'))
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE ID=%s", (session['user_id'],))
    user = cur.fetchone()
    cur.close()
    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        cur = mysql.connection.cursor()
        cur.execute("UPDATE users SET Firstname=%s, Lastname=%s WHERE ID=%s", (firstname, lastname, session['user_id']))
        mysql.connection.commit()
        cur.close()
        flash("Profile updated!")
        return redirect(url_for('profile.profile_page'))
    return render_template('profile.html', user=user)
