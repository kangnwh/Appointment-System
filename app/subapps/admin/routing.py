# -*- coding: utf-8 -*-
import datetime as dt
from functools import wraps
import hashlib,json

from flask import Blueprint, request, url_for, jsonify, redirect, current_app as app
from flask import render_template, flash, render_template_string
from flask_login import login_required

from app.models import *
from app.utli.forms import *

adminRoute = Blueprint('adminRoute', __name__,
                       template_folder='templates', static_folder='static')


def admin_only(func):
    @wraps(func)
    def innerFunc(*args, **kwargs):
        if not current_user.is_admin():
            return render_template_string("<h1 class='danger'>Only Administrator can access this page.</h1>"
                                          "<a href=" + url_for("homeRoute.index") + ">Back to Home Page</a>")
        else:
            return func(*args, **kwargs)

    return innerFunc


@adminRoute.route('/', methods=['GET'])
@login_required
@admin_only
def index():
    return redirect(url_for("adminRoute.appt"))


@adminRoute.route('/appt', methods=['GET', 'POST'])
@login_required
@admin_only
def appt():
    today = dt.date.today()
    date = request.args.get("date",today)
    session = Session()
    form = ApptForm()
    # appt_list = session.query(Appt).filter(Appt.appt_date == date).all()
    appt_list = appt_by_date(date)
    form.appt_service.choices = session.query(Service.id, Service.type).all()
    return render_template("admin/appt.html", form=form, appt_list=appt_list, current_page="appt",date=date)


@adminRoute.route('/service', methods=['GET', 'POST'])
@login_required
@admin_only
def service():
    session = Session()
    service_list = session.query(Service).all()
    form = ServiceForm()
    return render_template("admin/service.html", service_list=service_list, form=form,current_page = 'service')


@adminRoute.route('/service_delete/<int:service_id>', methods=['GET', 'POST'])
@login_required
@admin_only
def service_delete(service_id):
    session = Session()
    try:
        session.query(Service).filter(Service.id == service_id).delete()
        session.commit()
        session.close()
        flash("Delete successfully", "success")
    except Exception as e:
        flash("Delete failed", "danger")
        flash(e,"danger")
    return redirect(url_for("adminRoute.service"))


@adminRoute.route('/service_update', methods=['POST'])
@login_required
@admin_only
def service_update():
    form = ServiceForm()
    if form.validate_on_submit():
        id = form.id.data
        type = form.type.data
        desc = form.desc.data
        fee = form.fee.data

        try:
            session = Session()
            this_service_query = session.query(Service).filter(Service.id == id)
            if this_service_query.first():
                this_service_query.update(
                    {
                        "type": type,
                        "desc": desc,
                        "fee": fee
                    },
                    synchronize_session='evaluate'
                )
                session.commit()
                session.close()
                flash(("Service %s is updated successfully" % type), "success")
            else:
                flash(("Service %s does not exist" % type), "danger")
        except Exception  as e:
            flash("Update service information failed", "danger")
            flash(e)
            redirect(url_for("adminRoute.service"))

    return redirect(url_for("adminRoute.service"))


@adminRoute.route('/service_add', methods=['POST'])
@login_required
@admin_only
def service_add():
    form = ServiceForm()
    if form.validate_on_submit():
        type = form.type.data
        desc = form.desc.data
        fee = form.fee.data

        try:
            session = Session()
            this_service = Service(type, desc, fee)
            session.add(this_service)
            session.commit()
            session.close()
            flash("Add service information successfully", "success")
        except Exception  as e:
            flash("Add service information failed", "danger")
            flash(e)
            redirect(url_for("adminRoute.service"))

    return redirect(url_for("adminRoute.service"))


@adminRoute.route('/administrator', methods=['GET', 'POST'])
@login_required
@admin_only
def administrator():
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

        md5 = hashlib.md5()
        md5.update(form.password.data.encode('utf-8'))
        password = md5.hexdigest()

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
                    'email':email,
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
            # app.config["REMINDER_PRE"] = reminder_period

            flash("Update admin profile successfully", "success")
        except Exception  as e:
            flash("Update user profile failed", "danger")
            flash(e)
            return render_template('admin/administrator.html', form=form)
        return redirect(url_for('adminRoute.administrator'))
    return render_template('admin/administrator.html', form=form, current_page="admin")


@adminRoute.route('/reminder', methods=['GET', 'POST'])
@login_required
@admin_only
def reminder():
    form = ReminderForm()
    if form.validate_on_submit():
        reminder_period = form.reminder_period.data
        via_email = form.via_email.data
        via_message = form.via_message.data

        app.config['REMINDER_PRE'] = reminder_period
        app.config['VIA_EMAIL'] = via_email
        app.config['VIA_PHONE_MESSAGE'] = via_message
        flash("Update reminder information successfully","success")

    reminder_config = [app.config['REMINDER_PRE'],app.config['VIA_EMAIL'],app.config['VIA_PHONE_MESSAGE']]
    return render_template("admin/reminder.html",form=form,reminder_config=reminder_config,current_page="reminder")


# @adminRoute.route('/appt_by_date/', methods=['GET'])
@login_required
@admin_only
def appt_by_date(date):
    session = Session()
    # date = request.args.get("date")
    appt_list_all = session.query(Appt).filter(Appt.appt_date == date).order_by(Appt.id).all()
    overall_dict = dict()
    appt_list = list()
    for appt in appt_list_all:
        appt_dict = dict()
        appt_dict["id"] = appt.id
        appt_dict["user"] = appt.owner.first_name
        appt_dict["phone"] = appt.owner.phone

        address = dict()
        address["street"] = appt.owner.address.street
        address["city"] = appt.owner.address.city
        address["post_code"] = appt.owner.address.post_code

        appt_dict["address"] = address
        appt_dict["time"] = appt.appt_timeslot.slot
        appt_dict["status"] = appt.status

        pet_info = dict()
        pet_info["name"] = appt.pet.name
        pet_info["breed"] = appt.pet.breed
        pet_info["gender"] = appt.pet.gender
        pet_info["dob"] = appt.pet.dob.__str__()
        appt_dict["pet"] = pet_info

        services = list()
        for s in appt.appt_service:
            services.append(s.service.type)
        appt_dict["services"] = services
        appt_list.append(appt_dict)

    return appt_list


@adminRoute.route('/appt_finish', methods=['GET'])
@login_required
@admin_only
def appt_finish():
    appt_id = request.args.get("appt_id")
    date = request.args.get("date")
    session = Session()
    session.query(Appt).filter(Appt.id == appt_id).update({"status":"Done"})
    session.commit()
    session.close()
    return redirect(url_for("adminRoute.appt",date=date))
