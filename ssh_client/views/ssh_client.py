from flask import Blueprint, render_template, abort, flash
from flask import request

page = Blueprint('main', __name__, template_folder='templates')


@page.route("/",methods=['GET'])
def show_client():
    # flash("Grid loaded", 'success')
    return render_template('index.html')
