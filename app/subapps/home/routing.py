# -*- coding: utf-8 -*-
import hashlib, datetime

from flask import Blueprint, url_for, flash, request
from flask import render_template, redirect
from flask_login import login_user, logout_user, login_required, current_user

from app.models import User, Address, Pet
from app.db_info import Session
from app.subapps.home.forms import LoginForm, RegisterForm, UserProfileForm,PetForm

homeRoute = Blueprint('homeRoute', __name__,
                      template_folder='templates', static_folder='static')


@homeRoute.route('/', methods=['GET', 'POST'])
def index():
    return render_template('home/index.html', current_page="home")


@homeRoute.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # Login and validate the user.
        # user should be an instance of your `User` class
        email = form.email.data
        md5 = hashlib.md5()
        md5.update(form.password.data.encode('utf-8'))
        # password = md5.hexdigest()
        password = form.password.data
        user = User.query.filter_by(email=email, password=password).first()
        if user:
            login_user(user, remember=True)
            flash("Login Successfully.","success")
            next = request.args.get('next')
            return redirect(next or url_for('homeRoute.index'))

        else:
            flash("User ID or Password invalid.","danger")

    return render_template('home/login.html', form=form)


@homeRoute.route('/logout')
def logout():
    logout_user()
    return redirect(url_for("homeRoute.index"))


@homeRoute.route('/appointment')
@login_required
def appointment():
    return render_template('home/appointment.html', form=None, current_page="appointment")


@homeRoute.route('/pet')
@login_required
def pet():
    session = Session()
    pet_list = session.query(Pet).filter(Pet.owner_id == current_user.id).all()
    form = PetForm()
    return render_template('home/pet.html', form=form, current_page="pet",pet_list = pet_list)

@homeRoute.route('/pet_update')
@login_required
def pet_update():
    pass

@homeRoute.route('/pet_delete')
@login_required
def pet_delete():
    pass

@homeRoute.route('/user', methods=['GET', 'POST'])
@login_required
def user_update():
    form = UserProfileForm()
    if form.validate_on_submit():
        # address info
        # address_id = form.address_id.data
        city = form.city.data
        street = form.street.data
        post = form.post_code.data
        # address = Address(city, street, post_code=post)

        # User info
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data
        phone = form.phone.data
        home_numaber = form.home_number.data
        work_number = form.work_number.data
        gender = form.gender.data
        dob = form.dob.data

        # md5 = hashlib.md5()
        # md5.update(form.password.data.encode('utf-8')) # TODO encrypt password
        # password = md5.hexdigest()
        # password = form.password.data

        try:

            session = Session()
            session.query(Address).filter(Address.id == current_user.address.id).update(
                {
                    'city': city,
                    'street': street,
                    'post_code': post,
                },
                synchronize_session='evaluate'
            )
            session.query(User).filter(User.id == current_user.id).update(
                {
                    "first_name": first_name,
                    'last_name': last_name,
                    'phone':phone,
                    'home_number':home_numaber,
                    'work_number':work_number,
                    'dob': dob,
                    'gender': gender
                }
                , synchronize_session='evaluate'
            )
            # session.add(address)
            # session.add(user)
            session.commit()

        except Exception  as e:
            flash("Update user profile failed","danger")
            flash(e)
            return render_template('home/user.html', form=form)

        flash("Update Successfully.","success")
        next = request.args.get('next')
        return redirect(next or url_for('homeRoute.user_update'))
    return render_template('home/user.html', form=form, current_page="user")


@homeRoute.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        # address info
        city = form.city.data
        street = form.street.data
        post = form.post_code.data
        address = Address(city, street, post_code=post)

        # User info
        first_name = form.first_name.data
        last_name = form.last_name.data
        gender = form.gender.data
        dob = form.dob.data
        email = form.email.data
        phone = form.phone.data
        home_numaber = form.home_number.data
        work_number = form.work_number.data
        md5 = hashlib.md5()
        md5.update(form.password.data.encode('utf-8'))  # TODO encrypt password
        # password = md5.hexdigest()
        password = form.password.data
        user = User(email=email, password=password, first_name=first_name, last_name=last_name, dob=dob, gender=gender,
                    address=address,phone=phone,home_number=home_numaber,work_number=work_number)

        try:
            session = Session()
            session.add(address)
            session.add(user)
            session.commit()
        except Exception  as e:
            flash("Register Failed, check again later", "danger")
            flash(e)
            return render_template('home/register.html', form=form)

        login_user(user, remember=True)
        flash("Register Successfully.","success")
        next = request.args.get('next')
        return redirect(next or url_for('homeRoute.index'))

    return render_template('home/register.html', form=form)
