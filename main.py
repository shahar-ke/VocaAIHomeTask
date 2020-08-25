from app import app
from views.best_image_view import best_image_view
from views.display_view import display_view
from views.face_list_view import face_list_view
from views.index_view import index_view

app.register_blueprint(index_view)
app.register_blueprint(face_list_view)
app.register_blueprint(best_image_view)
app.register_blueprint(display_view)


@app.after_request
def add_header(response):
    response.headers['Pragma'] = 'no-cache'
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Expires'] = '0'
    return response


def main():
    app.run()


if __name__ == "__main__":
    main()
