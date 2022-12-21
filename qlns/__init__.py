from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import quote
from flask_login import LoginManager
from flask_babelex import Babel
import cloudinary

app = Flask(__name__, template_folder='templates')
app.secret_key = '689567gh$^^&*#%^&*^&%^*DFGH^&*&*^*'
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:%s@localhost/qlns?charset=utf8mb4" % quote('Admin@123')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['CART_KEY'] = 'cart'

cloudinary.config(cloud_name='dkfnlesea', api_key='841397193959693', api_secret='ZbKiAJ_qnDGZt1bfkIei9hRgceA')

db = SQLAlchemy(app=app)

login = LoginManager(app=app)

babel = Babel(app=app)


@babel.localeselector
def load_locale():
    return 'vi'
