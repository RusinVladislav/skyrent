import math

from flask import request
from flask_restx import Resource, Namespace

from app.container import place_services
from app.dao.models.place import PlaceSchema

place_ns = Namespace('places')
place_schema = PlaceSchema()


@place_ns.route('/')
class PlacesView(Resource):
    def get(self):
        try:
            places = place_schema.dump(place_services.get_all(), many=True)
            if request.args:
                city = request.args.get("city")
                minimum = request.args.get("from")
                maximum = request.args.get("to")
                if city:
                    places = [place for place in places if place["city"] == city]
                if minimum:
                    places = [place for place in places if int(place["price"]) >= int(minimum)]
                if maximum:
                    places = [place for place in places if int(place["price"]) <= int(maximum)]
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

        return [{"message": "Place delete", "pk": pk}], 204


# Дополнительная ручка для тестирования пагинации на фронте
@place_ns.route('/s/')
class PlacesView(Resource):
    def get(self):
        try:
            places = place_schema.dump(place_services.get_all(), many=True)
            if request.args:
                city = request.args.get("city")
                minimum = request.args.get("from")
                maximum = request.args.get("to")
                if city:
                    places = [place for place in places if place["city"] == city]
                if minimum:
                    places = [place for place in places if int(place["price"]) >= int(minimum)]
                if maximum:
                    places = [place for place in places if int(place["price"]) <= int(maximum)]

            # PAGINATION
            # задаем количество элементов на странице
            LIMIT_ITEMS_ON_PAGE = 5

            # получаем значение из адресной строки по ключу "page"
            item = request.args.get("page")

            # делаем проверку на полученное значение из адресной страницы
            if item is None:
                page_n = request.args.get("page", 1)
            elif item.isdigit():
                page_n = int(item)
            else:
                page_n = request.args.get("page", 1)

            # выводим необходимое количество элементов в зависимости от страницы путем среза из списка
            items_to_show = places[(page_n - 1) * LIMIT_ITEMS_ON_PAGE:page_n * LIMIT_ITEMS_ON_PAGE]

            # всего страниц
            all_pages = math.ceil(len(places) / 5)

            if page_n <= all_pages:
                return {
                            'data': items_to_show,
                            'pagination': {"pages": all_pages, "page": page_n, 'totalObjects': len(places)}
                }, 200
            else:
                page_n = all_pages
                items_to_show = places[(page_n - 1) * LIMIT_ITEMS_ON_PAGE:page_n * LIMIT_ITEMS_ON_PAGE]
                return {
                           'data': items_to_show,
                           'pagination': {"pages": all_pages, "page": all_pages, 'totalObjects': len(places)}
                       }, 200

        except Exception:
            return [{"message": "404 not found"}], 404

# специально для Вани
@place_ns.route('/n/')
class PlaceN(Resource):
    def get(self):
        return "5"


# дополнительная ручка для фронта со списком стран и городов
@place_ns.route('/filter_options/')
class PlacesView(Resource):
    def get(self):
        try:
            places = place_schema.dump(place_services.get_all(), many=True)
            list_pair = []
            for place in places:
                pair = (place['country'], place['city'])
                if pair not in list_pair:
                    list_pair.append(pair)
            filter_options = [{"country": pair[0], "city": pair[1]} for pair in list_pair]

            return filter_options, 200

        except Exception:
            return [{"message": "404 not found"}], 404


# дополнительная ручка по детальному отображению объекта
@place_ns.route('/s/<int:pk>')
class PlaceView(Resource):
    def get(self, pk: int):
        try:
            return {
                        'data': [place_schema.dump(place_services.get_one(pk))],
                        'pagination': {"pages": 1, "page": 1, 'totalObjects': 1}
            }, 200
        except Exception:
            return [{"message": "404 not found"}], 404

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
