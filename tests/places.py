from unittest.mock import MagicMock

import pytest
from app.dao.place import PlaceDAO
from app.dao.models.place import Place
from app.services.place import PlaceServices


@pytest.fixture()
def place_dao():
    place_init = PlaceDAO(None)

    place_1 = Place(
        pk=1,
        host_name="Alethea",
        host_location="1543 Agiou Konstantinou ",
        title="Suite on Agiou Konstantinou",
        features_off="AC, Netflix, an iron, fireplace, bike",
        host_phone="568-904-2568",
        price=400,
        picture_url="https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1680&q=80",
        country="Greece",
        description="The building is shaped like an L. The extension extends into stylish gardens reaching until the end of that side of the house.",
        city="Athens",
        features_on="Terrace, Fitness, Desk, Parking, WiFi",
    )

    place_2 = Place(
        pk=2,
        host_name="Alethea",
        host_location="1543 Agiou Konstantinou ",
        title="Suite on Agiou Konstantinou",
        features_off="AC, Netflix, an iron, fireplace, bike",
        host_phone="568-904-2568",
        price=400,
        picture_url="https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1680&q=80",
        country="Greece",
        description="The building is shaped like an L. The extension extends into stylish gardens reaching until the end of that side of the house.",
        city="Athens",
        features_on="Terrace, Fitness, Desk, Parking, WiFi",
    )
    place_init.get_one = MagicMock(return_value=place_1)
    place_init.get_all = MagicMock(return_value=[place_1, place_2])
    place_init.create = MagicMock(return_value=place_1)
    place_init.delete = MagicMock(return_value=True)
    place_init.update = MagicMock(return_value=True)

    return place_init


class TestPlaceServices:
    @pytest.fixture(autouse=True)
    def place_service(self, place_dao):
        self.place_service = PlaceServices(place_dao)

    def test_get_one(self):
        assert self.place_service.get_one(1) is not None
        assert self.place_service.get_one(1).title == "Suite on Agiou Konstantinou"

    def test_get_all(self):
        assert len(self.place_service.get_all()) == 2

    def test_delete(self):
        assert self.place_service.delete(1) is None

    def test_update(self):
        assert self.place_service.update(self.place_service.get_one(1)) is True
