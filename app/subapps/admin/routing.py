# -*- coding: utf-8 -*-
from flask import Blueprint, request, url_for
from flask import render_template
from flask_login import login_required



adminRoute = Blueprint('adminRoute', __name__,
                       template_folder='templates', static_folder='static')



@adminRoute.route('/', methods=['GET', 'POST'])
@login_required
def index():
    return render_template("admin/index.html")


@adminRoute.route('/login', methods=['GET', 'POST'])
@login_required
def login():
    return render_template("admin/index.html")