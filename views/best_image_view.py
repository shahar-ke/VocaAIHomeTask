import os
from typing import Dict
# noinspection PyPackageRequirements
from azure.cognitiveservices.vision.face import FaceClient
from flask import Blueprint, render_template
from flask_api import status
from msrest.authentication import CognitiveServicesCredentials

from app import app
from models.face import Face

best_image_view = Blueprint('best_image_view', __name__)
ENDPOINT = os.environ['FACE_ENDPOINT']
KEY = os.environ['FACE_SUBSCRIPTION_KEY']

counter = 0


def _extract_best_face(groups, face_map):
    groups.sort(key=lambda group: len(group), reverse=True)
    largest_group = groups[0]
    largest_group_faces = [face_map[face_id] for face_id in largest_group]
    largest_group_faces.sort(key=lambda face: face.area, reverse=True)
    best_face = largest_group_faces[0]
    return best_face


def _detect_faces(face_client):
    face_map: Dict[str, Face] = dict()
    upload_folder = app.config['UPLOAD_FOLDER']
    errors = list()
    for file in os.listdir(upload_folder):
        file_path = os.path.join(upload_folder, file)
        try:
            with open(file_path, 'rb') as image_stream:
                face_list = face_client.face.detect_with_stream(image_stream, return_face_id=True)
                for client_face in face_list:
                    face_map[client_face.face_id] = Face(face_client_obj=client_face, file=file)
        except Exception as e:
            logger.exceptiopn(e)
            logger.error('err msg')
            errors.append(file_path)
    return face_map, errors


@best_image_view.route('/get_best', methods=['GET'])
def get_best():
    try:
        # noinspection PyTypeChecker
        face_client = FaceClient(ENDPOINT, CognitiveServicesCredentials(KEY))
    except Exception as e:
        return render_template('error.html', error_msg=f'could not init face client: {str(e)}'), \
               status.HTTP_500_INTERNAL_SERVER_ERROR
    try:
        face_map, errors = _detect_faces(face_client)
        face_group = face_client.face.group(face_map.keys())
    except Exception as e:
        return render_template('error.html', error_msg=f'could not group faces: {str(e)}'), \
               status.HTTP_500_INTERNAL_SERVER_ERROR
    groups = face_group.groups
    if not groups:
        return render_template('error.html', error_msg='could not group faces'), \
               status.HTTP_500_INTERNAL_SERVER_ERROR
    best_face: Face = _extract_best_face(groups, face_map)
    return render_template('upload.html',
                           best_image=best_face.file,
                           rectangle_coordinates=best_face.rectangle_coord,
                           errors=errors), status.HTTP_200_OK
