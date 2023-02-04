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

    def post(self):
        req_json = request.json
        place_services.create(req_json)

        return "Place add", 201


@place_ns.route('/<int:pk>')
class PlaceView(Resource):
    def get(self, pk: int):
        try:
            place = place_services.get_one(pk)
            return place_schema.dump(place), 200
        except Exception:
            return "", 404

    # def put(self, pk: int):
    #     req_json = request.json
    #     req_json['pk'] = pk
    #     place_services.update(req_json)
    #
    #     return "Place put", 204
    #
    # def patch(self, pk: int):
    #     req_json = request.json
    #     req_json['pk'] = pk
    #     place_services.update_partial(req_json)
    #
    #     return "Place patch", 204
    #
    # def delete(self, pk: int):
    #     place_services.delete(pk)
    #
    #     return "Place delete", 204
