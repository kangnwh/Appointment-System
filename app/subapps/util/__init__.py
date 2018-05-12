from flask import flash,render_template_string,url_for
from flask_login import current_user


def flash_form_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ))


