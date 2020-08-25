from flask import Blueprint, render_template

index_view = Blueprint('index_view', __name__)


@index_view.route('/', methods=['GET', 'POST'])
def index():
    return render_template('upload.html')
