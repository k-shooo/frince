from flask import Flask
from flask_mysqldb import MySQL
from flask_mail import Mail

app = Flask(__name__)
app.secret_key = "your_secret_key"

# MySQL Config
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'personal_website'
mysql = MySQL(app)

# Mail Config
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'your_email@gmail.com'
app.config['MAIL_PASSWORD'] = 'your_app_password'
mail = Mail(app)

# Blueprints
from app.routes.auth import auth
from app.routes.dashboard import dashboard
from app.routes.profile import profile
from app.routes.blog import blog
from app.routes.game import games as games_bp

app.register_blueprint(auth)
app.register_blueprint(dashboard)
app.register_blueprint(profile)
app.register_blueprint(blog)
app.register_blueprint(games_bp)

