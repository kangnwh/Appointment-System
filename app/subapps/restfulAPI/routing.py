# -*- coding: utf-8 -*-
import hashlib, datetime as dt

from flask import Blueprint, url_for, flash, request, jsonify
from flask import render_template, redirect
from flask_login import login_user, logout_user, login_required, current_user

from app.models import *
from app.db_info import Session
from app.subapps.home.forms import *

restRoute = Blueprint('restRoute', __name__,
                      template_folder='templates', static_folder='static')


@restRoute.route('/timeslot/', methods=['GET'])
# @login_required
def timeslot():
    session = Session()
    date = request.args.get("date")
    not_available = session.query(Appt.appt_timeslot_id).filter(Appt.appt_date == date).all()
    not_in = [value for value, in not_available]
    available = session.query(ApptTimeSlot.id,ApptTimeSlot.slot).filter(~ApptTimeSlot.id.in_(not_in)).all()
    return jsonify(list = available)

