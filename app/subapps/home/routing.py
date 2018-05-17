# -*- coding: utf-8 -*-
import hashlib

from flask import Blueprint, url_for, flash, request
from flask import render_template, redirect
from flask_login import login_user, logout_user, login_required

from app.models import *
from app.utli.forms import *

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
        password = md5.hexdigest()
        user = User.query.filter_by(email=email, password=password).first()
        if user:
            login_user(user, remember=True)
            flash("Login Successfully.", "success")
            next = request.args.get('next')
            return redirect(next or url_for('homeRoute.index'))

        else:
            flash("User ID or Password invalid.", "danger")
    next = request.args.get('next')
    return render_template('home/login.html', form=form,next=next)


@homeRoute.route('/logout')
def logout():
    logout_user()
    return redirect(url_for("homeRoute.index"))


@homeRoute.route('/pet')
@login_required
def pet():
    session = Session()
    pet_list = session.query(Pet).filter(Pet.owner_id == current_user.id).all()
    form = PetForm()
    return render_template('home/pet.html', form=form, current_page="user", pet_list=pet_list, user_tab="pet")


@homeRoute.route('/pet_add', methods=['POST'])
@login_required
def pet_add():
    form = PetForm()
    if form.validate_on_submit():
        name = form.name.data
        breed = form.breed.data
        gender = form.gender.data
        dob = form.dob.data

        try:
            session = Session()
            this_pet = Pet(current_user, name, breed, gender, dob)
            session.add(this_pet)
            session.commit()
            session.close()
            flash("Add pet sucessfully", "success")
        except Exception  as e:
            flash("Add pet failed", "danger")
            flash(e)
            redirect(url_for("homeRoute.pet"))
        return redirect(url_for("homeRoute.pet"))
    flash("Add pet failed", "danger")
    return redirect(url_for("homeRoute.pet"))


@homeRoute.route('/pet_update', methods=['POST'])
@login_required
def pet_update():
    form = PetForm()
    if form.validate_on_submit():
        id = form.id.data
        name = form.name.data
        breed = form.breed.data
        gender = form.gender.data
        dob = form.dob.data

        try:
            session = Session()
            this_pet = session.query(Pet).filter(Pet.id == id, Pet.owner_id == current_user.id)
            if this_pet.count() > 0:
                this_pet.update(
                    {
                        'name': name,
                        'breed': breed,
                        'gender': gender,
                        'dob': dob,
                    },
                    synchronize_session='evaluate'
                )
                session.commit()
                session.close()
            else:
                flash(("Pet %s is not found under user %s" % name, current_user.email), "danger")

        except Exception  as e:
            flash("Update pet information failed", "danger")
            flash(e)
            redirect(url_for("homeRoute.pet"))

        flash("Update pet information Successfully.", "success")
        return redirect(url_for("homeRoute.pet"))
    return redirect(url_for("homeRoute.pet"))


@homeRoute.route('/pet_delete/<int:pet_id>', methods=['GET'])
@login_required
def pet_delete(pet_id):
    session = Session()
    this_pet = session.query(Pet).filter(Pet.id == pet_id, Pet.owner_id == current_user.id)
    if this_pet.count() > 0:
        this_pet.delete()
        session.commit()
        session.close()
        flash(("Pet %d is deleted successfully" % pet_id), "success")
    else:
        flash(("Pet %d is not found under user %s" % pet_id, current_user.email), "danger")
    return redirect(url_for("homeRoute.pet"))


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
                    'phone': phone,
                    'home_number': home_numaber,
                    'work_number': work_number,
                    'dob': dob,
                    'gender': gender
                }
                , synchronize_session='evaluate'
            )

            session.commit()
            session.close()

        except Exception  as e:
            flash("Update user profile failed", "danger")
            flash(e)
            return render_template('home/user.html', form=form)

        flash("Update Successfully.", "success")
        next = request.args.get('next')
        return redirect(next or url_for('homeRoute.user_update'))
    return render_template('home/user.html', form=form, current_page="user", user_tab="user")


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
        md5.update(form.password.data.encode('utf-8'))
        password = md5.hexdigest()

        user = User(email=email, password=password, first_name=first_name, last_name=last_name, dob=dob, gender=gender,
                    address=address, phone=phone, home_number=home_numaber, work_number=work_number)

        try:
            session = Session()
            session.add(address)
            session.add(user)
            session.commit()
            user = session.query(User).filter(User.email == email).first()
            session.close()
            login_user(user, remember=True)
        except Exception  as e:
            flash("Register Failed, check again later", "danger")
            flash(e)
            return render_template('home/register.html', form=form)

        flash("Register Successfully.", "success")
        next = request.args.get('next')
        return redirect(next or url_for('homeRoute.index'))

    return render_template('home/register.html', form=form)


@homeRoute.route('/card')
@login_required
def card():
    session = Session()
    card_list = session.query(Card).filter(Card.owner_id == current_user.id).all()
    form = CardForm()
    return render_template('home/card.html', form=form, current_page="user", card_list=card_list, user_tab="card")


@homeRoute.route('/card_add', methods=['POST'])
@login_required
def card_add():
    form = CardForm()
    if form.validate_on_submit():
        card_num = form.card_num.data
        bank = form.bank.data

        try:
            session = Session()
            this_card = Card(current_user, card_num, bank)
            session.add(this_card)
            session.commit()
            session.close()
            flash("Add Card sucessfully", "success")
        except Exception  as e:
            flash("Add card failed", "danger")
            flash(e)
            redirect(url_for("homeRoute.card"))
        return redirect(url_for("homeRoute.card"))
    flash("Add card failed", "danger")
    return redirect(url_for("homeRoute.card"))


@homeRoute.route('/card_update', methods=['POST'])
@login_required
def card_update():
    form = CardForm()
    if form.validate_on_submit():
        id = form.id.data
        card_num = form.card_num.data
        bank = form.bank.data

        try:
            session = Session()
            this_card = session.query(Card).filter(Card.id == id, Card.owner_id == current_user.id)
            if this_card.count() > 0:
                this_card.update(
                    {
                        'card_num': card_num,
                        'bank': bank
                    },
                    synchronize_session='evaluate'
                )
                session.commit()
                session.close()
            else:
                flash(("Card is not found under user %s" % current_user.email), "danger")

        except Exception  as e:
            flash("Update Card information failed", "danger")
            flash(e)
            redirect(url_for("homeRoute.card"))

        flash("Update Card information Successfully.", "success")
        return redirect(url_for("homeRoute.card"))
    return redirect(url_for("homeRoute.card"))


@homeRoute.route('/card_delete/<int:card_id>', methods=['GET'])
@login_required
def card_delete(card_id):
    session = Session()
    this_card = session.query(Card).filter(Card.id == card_id, Card.owner_id == current_user.id)
    if this_card.count() > 0:
        this_card.delete()
        session.commit()
        session.close()
        flash(("Card is deleted successfully"), "success")
    else:
        flash(("Card is not found under user %s" % current_user.email), "danger")
    return redirect(url_for("homeRoute.card"))


@homeRoute.route('/appointment', methods=['GET'])
@login_required
def appt():
    session = Session()
    form = ApptForm()
    appt_list = session.query(Appt).filter(Appt.owner_id == current_user.id).all()
    form.appt_service.choices = session.query(Service.id, Service.type).all()
    return render_template("home/appt_list.html", form=form, appt_list=appt_list, appt_tab="my",
                           current_page="appointment")


@homeRoute.route('/appt_update/', methods=['GET','POST'])
@login_required
def appt_update():
    form = ApptForm()
    if form.validate_on_submit():
        id = form.id.data
        appt_date = form.appt_date.data
        appt_timeslot = form.appt_timeslot.data
        appt_service = form.appt_service.data
        pet_id = form.pet.data
        try:
            session = Session()
            this_appt_query = session.query(Appt).filter(Appt.id == id, Appt.owner_id == current_user.id)
            this_appt = this_appt_query.first()
            if this_appt:
                this_appt_query.update(
                    {
                        'appt_date': appt_date,
                        'appt_timeslot_id': appt_timeslot,
                        'pet_id':pet_id
                    },
                    synchronize_session='evaluate'
                )
                session.query(Appt2Ser).filter(Appt2Ser.appt_id == id).delete()

                for s in appt_service:
                    appt2ser = Appt2Ser(this_appt,s)
                    session.add(appt2ser)

                session.commit()
                session.close()
            else:
                flash(("Appointment is not found under user %s" % current_user.email), "danger")

        except Exception as e:
            flash("Reschedule failed", "danger")
            flash(e)
            redirect(url_for("homeRoute.appt"))

        flash("Reschedule Successfully.", "success")
        return redirect(url_for("homeRoute.appt"))

    session = Session()
    appt_id = request.args.get('appt_id')
    if (appt_id):
        appt_info = session.query(Appt).filter(Appt.id == appt_id, Appt.owner_id == current_user.id).first()
        if(appt_info):
            form.appt_timeslot.choices = session.query(ApptTimeSlot.id,ApptTimeSlot.slot).order_by(ApptTimeSlot.id).all()
            selected_services = [ service.service_id for service in appt_info.appt_service ]
            form.pet.choices = session.query(Pet.id, Pet.name).filter(Pet.owner_id == current_user.id).all()

            return render_template("home/appt_update.html",
                                   form=form,
                                   appt_info=appt_info,selected_services = selected_services,
                               current_page='appointment',
                               appt_tab="my")
        else:
            flash(("Appointment is not found under user %s" % current_user.email), "danger")
            return redirect(url_for("homeRoute.appt"))
    return redirect(url_for("homeRoute.appt"))


@homeRoute.route('/appt_delete/<int:appt_id>', methods=['GET'])
@login_required
def appt_delete(appt_id):
    session = Session()
    this_appt = session.query(Appt).filter(Appt.id == appt_id, Appt.owner_id == current_user.id)
    if this_appt.count() > 0:
        this_appt.delete()
        session.commit()
        session.close()
        flash(("Appointment is deleted successfully"), "success")
    else:
        flash(("Appointment is not found under user %s" % current_user.email), "danger")
    return redirect(url_for("homeRoute.appt"))

@homeRoute.route('/appt_add', methods=['GET','POST'])
@login_required
def appt_add():
    form = ApptForm()
    if form.validate_on_submit():
        appt_date = form.appt_date.data
        appt_timeslot_id = form.appt_timeslot.data
        appt_service = form.appt_service.data
        pet_id = form.pet.data
        try:
            session = Session()
            new_appt = Appt(current_user.id,pet_id,appt_date,appt_timeslot_id)
            session.add(new_appt)
            for s in appt_service:
                appt2ser = Appt2Ser(new_appt, s)
                session.add(appt2ser)

            session.commit()
            session.close()

        except Exception  as e:
            flash("Make appointment failed", "danger")
            flash(e)
            redirect(url_for("homeRoute.appt"))

        flash("Reschedule Successfully.", "success")
        return redirect(url_for("homeRoute.appt"))

    session = Session()
    form.pet.choices = session.query(Pet.id,Pet.name).filter(Pet.owner_id == current_user.id).all()
    return render_template("home/appt_new.html",
                           form=form,
                           current_page='appointment',
                           appt_tab="new")