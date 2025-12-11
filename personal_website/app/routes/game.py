from flask import Blueprint, session, flash, redirect, url_for
import subprocess
from app import mysql

games = Blueprint('games', __name__)

@games.route('/games/play')
def play_game():
    if 'loggedin' not in session:
        return redirect(url_for('auth.login'))
    cur = mysql.connection.cursor()
    cur.execute("SELECT GameAccess FROM users WHERE ID=%s", (session['user_id'],))
    access = cur.fetchone()[0]
    cur.close()
    if access != 'enabled':
        flash("Your access to the game is disabled by admin.")
        return redirect(url_for('dashboard.user_dashboard'))
    subprocess.Popen(["python", "games/my_game.py"])
    flash("Game Launched!")
    return redirect(url_for('dashboard.user_dashboard'))
