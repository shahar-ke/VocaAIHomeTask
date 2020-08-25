import os

from PIL import Image, ImageDraw
from flask import url_for, Blueprint
from werkzeug.utils import redirect

from app import app

display_view = Blueprint('display_view', __name__)


@app.route('/display_error', methods=['GET', 'POST'])
def display_error():
    error_file = './errors/error.png'
    return redirect(url_for('static', filename=error_file), code=301)


@app.route('/display/<filename>/<rectangle_coordinates>', methods=['GET', 'POST'])
def display_image(filename, rectangle_coordinates):
    file_path_for_app = os.path.join('uploads/', filename)
    rectangle_coordinates = eval(rectangle_coordinates)
    if rectangle_coordinates:
        file_path_for_img = os.path.join('./static/uploads', filename)
        img = Image.open(file_path_for_img)
        draw = ImageDraw.Draw(img)
        draw.rectangle(rectangle_coordinates, outline='red', width=15)  # outline faces
        img.save(file_path_for_img)
    return redirect(url_for('static', filename=file_path_for_app), code=301)
