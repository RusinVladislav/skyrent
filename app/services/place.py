from app.dao.place import PlaceDAO


class PlaceServices:
    def __init__(self, dao: PlaceDAO):
        self.dao = dao

    def get_all(self):
        return self.dao.get_all()

    def get_one(self, pk):
        return self.dao.get_one(pk)

    def create(self, data):

        return self.dao.create(data)

    def update(self, data):
        pk = data.get("pk")
        place = self.get_one(pk)

        place.title = data.get('title')
        place.description = data.get('description')
        place.picture_url = data.get('picture_url')
        place.price = data.get('price')
        place.country = data.get('country')
        place.city = data.get('city')
        place.features_on = data.get('features_on')
        place.features_off = data.get('features_off')
        place.host_name = data.get('host_name')
        place.host_phone = data.get('host_phone')
        place.host_location = data.get('host_location')

        self.dao.update(place)

    def update_partial(self, data):
        pk = data.get("pk")
        place = self.get_one(pk)

        if "title" in data:
            place.title = data.get('title')
        if "description" in data:
            place.description = data.get('description')
        if "picture_url" in data:
            place.picture_url = data.get('picture_url')
        if "price" in data:
            place.price = data.get('price')
        if "country" in data:
            place.country = data.get('country')
        if "city" in data:
            place.city = data.get('city')
        if "features_on" in data:
            place.features_on = data.get('features_on')
        if "features_off" in data:
            place.features_off = data.get('features_off')
        if "host_name" in data:
            place.host_name = data.get('host_name')
        if "host_phone" in data:
            place.host_phone = data.get('host_phone')
        if "host_location" in data:
            place.host_location = data.get('host_location')

        self.dao.update(place)

    def delete(self, pk):
        self.dao.delete(pk)
