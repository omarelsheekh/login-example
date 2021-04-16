from flask.helpers import url_for
from admin import create_admin
from auth import auth_blueprint
from user import user as user_blueprint
from models import setup_db
from flask import Flask, redirect
from flask_migrate import Migrate, migrate
from models import UserModel
from flask_login import LoginManager
from werkzeug.security import generate_password_hash
import os

DB_IP=os.getenv('db_ip')
DB_USERNAME=os.getenv('db_username', 'db_user')
DB_NAME=os.getenv('db_name', 'test_db')
DB_USERPASS=os.getenv('db_userpass', 'db_pass')
DB_PORT=os.getenv('db_port', 5432)
SECRET_KEY=os.getenv('secret_key', 'secret')

app=Flask(__name__)
app.secret_key=SECRET_KEY
db=None
if DB_IP:
    database_path = 'postgresql://{username}:{passwd}@{host_ip}:{db_port}/{db_name}'.format(
        username=DB_USERNAME, passwd=DB_USERPASS, host_ip=DB_IP, db_name=DB_NAME, db_port=DB_PORT
    )
    db = setup_db(app, database_path)
    migrate = Migrate(app, db)
else:
    database_path = 'sqlite:////tmp/test.db'
    db = setup_db(app, database_path)
    db.drop_all()
    db.create_all()
# both bluprint is constructed different ways
app.register_blueprint(auth_blueprint(db), url_prefix='/auth')
app.register_blueprint(user_blueprint, url_prefix='/user')

admin = create_admin(app, db)
# create admin user
ADMIN_EMAIL=os.getenv('admin_email', 'admin@omar.com')
ADMIN_PASSWORD=os.getenv('admin_password', 'admin')
admin_user = UserModel(email=ADMIN_EMAIL, name='Admin', password=generate_password_hash(ADMIN_PASSWORD, method='sha256'), is_admin=True)
db.session.add(admin_user)
db.session.commit()

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return UserModel.query.get(int(user_id))


@app.route('/')
def index():
    return redirect(url_for('user.profile'))

@app.route('/status')
def running():
    return 'app is running'

if __name__ == "__main__":
    app.run(port=8000, debug=True, host='0.0.0.0')