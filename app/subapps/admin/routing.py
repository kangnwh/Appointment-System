# -*- coding: utf-8 -*-
from flask import Blueprint, request, url_for, jsonify, redirect, json
from flask import render_template, flash, render_template_string
from flask_login import login_required, current_user
from functools import wraps
from app.db_info import Session
import datetime as dt
from app.models import *
from app.subapps.admin.forms import *
from app.subapps.home.forms import *

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
    session = Session()
    form = ApptForm()
    appt_list = session.query(Appt).filter(Appt.appt_date == today).all()

    form.appt_service.choices = session.query(Service.id, Service.type).all()
    return render_template("admin/appt.html", form=form, appt_list=appt_list, current_page="appt")


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


@adminRoute.route('/reminder', methods=['GET', 'POST'])
@login_required
@admin_only
def reminder():
    return render_template("admin/appt.html")


@adminRoute.route('/adminstrator', methods=['GET', 'POST'])
@login_required
@admin_only
def admin():
    return render_template("admin/appt.html")


@adminRoute.route('/appt_by_date/', methods=['GET'])
@login_required
@admin_only
def appt_by_date():
    session = Session()
    date = request.args.get("date")
    appt_list_all = session.query(Appt).filter(Appt.appt_date == date).order_by(Appt.id).all()
    appt_list = list()
    for appt in appt_list_all:
        appt_dict = dict()
        appt_dict["id"] = appt.id
        appt_dict["user"] = appt.owner.first_name
        appt_dict["phone"] = appt.owner.phone
        appt_dict["address"] = appt.owner.address.__str__()
        appt_dict["time"] = appt.appt_timeslot.slot
        appt_dict["status"] = appt.status
        services = list()
        for s in appt.appt_service:
            services.append(s.service.type)
        appt_dict["services"] = services
        appt_list.append(appt_dict)

    return jsonify(list=appt_list)


@adminRoute.route('/appt_finish', methods=['GET'])
@login_required
@admin_only
def appt_finish():
    pass
