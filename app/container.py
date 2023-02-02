from app.dao.place import PlaceDAO
from app.database import db
from app.services.place import PlaceServices

place_dao = PlaceDAO(db.session)
place_services = PlaceServices(place_dao)
