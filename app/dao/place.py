from app.dao.models.place import Place


class PlaceDAO:
    def __init__(self, session):
        self.session = session

    def get_one(self, pk):
        return self.session.query(Place).get(pk)

    def get_all(self):
        return self.session.query(Place).all()

    def create(self, data):
        place = Place(**data)

        self.session.add(place)
        self.session.commit()

        return place

    def update(self, place):
        self.session.add(place)
        self.session.commit()

        return place

    def delete(self, pk):
        place = self.get_one(pk)

        self.session.delete(place)
        self.session.commit()
