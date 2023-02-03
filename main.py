from flask import Flask
from flask_restx import Api
from flask_cors import CORS

from app.dao.models.place import Place
from app.views.places import place_ns
from app.config import Config
from app.database import db
from data_file import PLACES_FILE
from utils import load_data


def create_app(config: Config) -> Flask:
    application = Flask(__name__)
    CORS(application)
    application.config.from_object(config)
    application.app_context().push()

    return application


def configure_app(application: Flask):
    db.init_app(application)
    api = Api(app)
    api.add_namespace(place_ns)

    # заполняем базу данных(таблицу Place) данными
    db.drop_all()
    db.create_all()
    places = load_data(PLACES_FILE)
    for place in places:
        place = Place(
            pk=place['pk'],
            title=place['title'],
            description=place['description'],
            picture_url=place['picture_url'],
            price=place['price'],
            country=place['country'],
            city=place['city'],
            features_on=place['features_on'],
            features_off=place['features_off'],
        )
        db.session.add(place)
        db.session.commit()


if __name__ == '__main__':
    app = create_app(Config())
    configure_app(app)
    app.run()
