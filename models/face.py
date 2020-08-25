class Face:

    def __init__(self, face_client_obj, file: str):
        self.file = file
        rectangle_data = self._get_rectangle_data(face_client_obj)
        self.rectangle_coord = rectangle_data[0]
        self.area = rectangle_data[1]

    @classmethod
    def _get_rectangle_data(cls, face_client_obj):
        left = face_client_obj.face_rectangle.left
        top = face_client_obj.face_rectangle.top
        bottom = left + face_client_obj.face_rectangle.height
        right = top + face_client_obj.face_rectangle.width
        area = face_client_obj.face_rectangle.height * face_client_obj.face_rectangle.width
        return ((left, top), (bottom, right)), area
