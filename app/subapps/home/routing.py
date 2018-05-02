 # -*- coding: utf-8 -*-
import hashlib,datetime

from flask import Blueprint,url_for,flash,request
from flask import render_template,redirect
from flask_login import login_user,logout_user,login_required

from app.models import User,Address
from app.db_info import Session
from app.subapps.home.forms import LoginForm,RegisterForm
homeRoute = Blueprint('homeRoute', __name__,
                     template_folder='templates', static_folder='static')


@homeRoute.route('/', methods=['GET', 'POST'])
def index():

    return render_template('home/index.html',current_page="home")

@homeRoute.route('/login',methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # Login and validate the user.
        # user should be an instance of your `User` class
        email = form.email.data
        md5 = hashlib.md5()
        md5.update(form.password.data.encode('utf-8'))
        #password = md5.hexdigest()
        password = form.password.data
        user = User.query.filter_by(email=email,password=password).first()
        if user :
            login_user(user,remember = True)
            flash("Login Successfully.")
            next = request.args.get('next')
            return redirect(next or url_for('homeRoute.index'))

        else:
            flash("User ID or Password invalid.")

    return render_template('home/login.html', form=form)


@homeRoute.route('/logout')
def logout():

    logout_user()
    return redirect(url_for("homeRoute.index"))


@homeRoute.route('/appointment')
@login_required
def appointment():
    return render_template('home/appointment.html', form=None,current_page="appointment")


@homeRoute.route('/pet')
@login_required
def pet():
    return render_template('home/pet.html', form=None,current_page="pet")


@homeRoute.route('/user')
@login_required
def user():
    return render_template('home/user.html', form=None,current_page="user")


@homeRoute.route('/register',methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        # address info
        city = form.city.data
        street = form.street.data
        post = form.post_code.data
        address = Address(city, street, post_code=post)

        # User info
        email = form.email.data
        md5 = hashlib.md5()
        md5.update(form.password.data.encode('utf-8'))
        #password = md5.hexdigest()
        password = form.password.data
        user = User(email=email,password=password,address=address)

        try:
            session = Session()
            session.add(address)
            session.add(user)
            session.commit()
        except Exception  as e:
            flash("Register Failed, check again later","danger")
            flash(e)
            return render_template('home/register.html', form=form)

        login_user(user,remember = True)
        flash("Register Successfully.")
        next = request.args.get('next')
        return redirect(next or url_for('homeRoute.index'))

    return render_template('home/register.html', form=form)