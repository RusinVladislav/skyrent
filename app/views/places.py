from flask import request
from flask_restx import Resource, Namespace

from app.container import place_services
from app.database import db
from app.dao.models.place import PlaceSchema, Place

place_ns = Namespace('places')
place_schema = PlaceSchema()


@place_ns.route('/')
class PlacesView(Resource):
    def get(self):
        try:
            if request.args:
                city = request.args.get("city")
                minimum = request.args.get("from")
                maximum = request.args.get("to")
                places = []
                if city:
                    result = db.session.query(Place).filter_by(city=city).all()
                    places.extend(place_schema.dump(result, many=True))
                else:
                    places = place_schema.dump(place_services.get_all(), many=True)
                if minimum:
                    places = [place for place in places if int(place["price"]) >= int(minimum)]
                if maximum:
                    places = [place for place in places if int(place["price"]) <= int(maximum)]
            else:
                return place_schema.dump(place_services.get_all(), many=True)

            return places, 200

        except Exception:
            return [{"message": "404 not found"}], 404

    def post(self):
        req_json = request.json
        new = place_services.create(req_json)

        return [{"message": "Place add", "pk": new.pk}], 201


@place_ns.route('/<int:pk>')
class PlaceView(Resource):
    def get(self, pk: int):
        try:
            place = place_services.get_one(pk)
            return [place_schema.dump(place)], 200
        except Exception:
            return [{"message": "404 not found"}], 404

    def put(self, pk: int):
        req_json = request.json
        req_json['pk'] = pk
        place_services.update(req_json)

        return [{"message": "Place put", "pk": pk}], 201

    def patch(self, pk: int):
        req_json = request.json
        req_json['pk'] = pk
        place_services.update_partial(req_json)

        return [{"message": "Place patch", "pk": pk}], 201

    def delete(self, pk: int):
        place_services.delete(pk)

        return "Place delete", 204

# попытка реализовать автоматическую перезаливку приложения на сервер после комита
# https://habr.com/en/post/457348/
# @place_ns.route('/update_server', methods=['POST'])
# def webhook():
#     if request.method == 'POST':
#         repo = git.Repo('https://github.com/RusinVladislav/skyrent')
#         origin = repo.remotes.origin
#         origin.pull()
#         return 'UpdatePythonAnywhere successfully', 200
#     else:
#         return 'Wrong event type', 400
