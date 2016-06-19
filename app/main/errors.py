from flask import render_template
from . import main

@main.app_errorhandler(404)
def page_not_found(e):
    # return render_template('404.html'), 404
    return '404 son, page not found'

@main.app_errorhandler(500)
def internal_server_error(e):
    # return render_template('500.html'), 500
    return '500 error, woah shit'
