# project/client/views.py

"""RESTful API Client"""

from flask import Blueprint, render_template


views_blueprint = Blueprint('views', __name__, template_folder='./templates')


"""Primary user interface"""
@views_blueprint.route('/', methods=['GET'])
def index():
    return render_template('main.html')
