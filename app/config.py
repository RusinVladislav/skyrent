class Config:
    FLASK_DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///place.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSONIFY_PRETTYPRINT_REGULAR = True
    RESTX_JSON = {'ensure_ascii': False}
