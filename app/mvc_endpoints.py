from flask import Blueprint, render_template, redirect, url_for

from app import bcrypt
from app.data_classes import Service, News
from app.forms import LoginForm, RegisterForm
from app.models import db, User
from flask_login import login_user, login_required, logout_user

from app.utils import load_json

mvc_bp = Blueprint('mvc', __name__)


@mvc_bp.route('/')
def index():
    return render_template("index.html")


@mvc_bp.route('/services')
def services():
    services_data = load_json('static/json/services.json')
    services_list = [Service(**service) for service in services_data]
    return render_template('Services.html', services=services_list)

@mvc_bp.route('/news')
def news():
    news_data = load_json('static/json/news.json')
    news_items = [News(**news) for news in news_data]
    return render_template('News.html', news_items=news_items)


@mvc_bp.route('/career')
def career():
    return render_template("Career.html")


@mvc_bp.route('/about-us')
def about_us():
    return render_template("About-us.html")


@mvc_bp.route('/contact')
def contact():
    return render_template("Contact.html")


@mvc_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('mvc.index'))
    return render_template("Login.html", form=form)


@mvc_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        user = User(email=form.email.data, password=hashed_password, name=form.name.data, last_name=form.last_name.data,
                    company_name=form.company_name.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('mvc.login'))

    return render_template("Register.html", form=form)


@mvc_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('mvc.index'))


@mvc_bp.route('/my_routes')
@login_required
def dashboard():
    print("here")
    return render_template('My_Routes.html')
