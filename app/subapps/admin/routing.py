# -*- coding: utf-8 -*-
from flask import Blueprint, request, url_for
from flask import render_template,flash,render_template_string
from flask_login import login_required,current_user



adminRoute = Blueprint('adminRoute', __name__,
                       template_folder='templates', static_folder='static')



def admin_only(func):
    if (not current_user.is_admin()):
        return render_template_string("<h1 class='danger'>Only Administrator can access this page.</h1>"
                                      "<a href=" + url_for("homeRoute.index") + ">Back to Home Page</a>")
    else:
        return func()

@adminRoute.route('/', methods=['GET', 'POST'])
@login_required
def index():
    if(not current_user.is_admin()):
        return render_template_string("<h1 class='danger'>Only Administrator can access this page.</h1>"
                                      "<a href="+url_for("homeRoute.index")+">Back to Home Page</a>")


    return render_template("admin/index.html")


@adminRoute.route('/login', methods=['GET', 'POST'])
@login_required
def login():
    return render_template("admin/index.html")