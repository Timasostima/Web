from flasgger import Swagger
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

from app.models import User

bcrypt = Bcrypt()
login_manager = LoginManager()
swagger = Swagger()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
