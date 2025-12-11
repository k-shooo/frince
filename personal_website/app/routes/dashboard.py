from flask import Blueprint, render_template, session, redirect, url_for, flash
from app import mysql

dashboard = Blueprint('dashboard', __name__)

@dashboard.route('/dashboard/user')
def user_dashboard():
    if 'loggedin' in session and session['role']=='User':
        return render_template('dashboard_user.html')
    return redirect(url_for('auth.login'))

@dashboard.route('/dashboard/admin')
def admin_dashboard():
    if 'loggedin' in session and session['role']=='admin':
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users")
        users = cur.fetchall()
        cur.close()
        return render_template('dashboard_admin.html', users=users)
    return redirect(url_for('auth.login'))

@dashboard.route('/admin/toggle_status/<int:user_id>')
def toggle_status(user_id):
    if 'loggedin' in session and session['role']=='admin':
        cur = mysql.connection.cursor()
        cur.execute("SELECT Status FROM users WHERE ID=%s", (user_id,))
        status = cur.fetchone()[0]
        new_status = 'inactive' if status=='active' else 'active'
        cur.execute("UPDATE users SET Status=%s WHERE ID=%s", (new_status,user_id))
        mysql.connection.commit()
        cur.close()
        flash(f'User status changed to {new_status}.')
    return redirect(url_for('dashboard.admin_dashboard'))

@dashboard.route('/admin/toggle_game/<int:user_id>')
def toggle_game(user_id):
    if 'loggedin' in session and session['role']=='admin':
        cur = mysql.connection.cursor()
        cur.execute("SELECT GameAccess FROM users WHERE ID=%s", (user_id,))
        current = cur.fetchone()[0]
        new_access = 'disabled' if current=='enabled' else 'enabled'
        cur.execute("UPDATE users SET GameAccess=%s WHERE ID=%s", (new_access,user_id))
        mysql.connection.commit()
        cur.close()
        flash(f'Game access for user updated to {new_access}.')
    return redirect(url_for('dashboard.admin_dashboard'))
