import os

from flask import Flask
from flask_smorest import Api
# from flask_migrate import Migrate

# from dotenv import load_dotenv

# from db import db
# import models

# from resources.user import blp as UserBluePrint
from resources.availability import blp as AvailabilityBluePrint

def create_app(db_url=None):
    app = Flask(__name__)
    # load_dotenv()

    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Tripstick API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    # app.config['SQLALCHEMY_DATABASE_URI'] = db_url or os.getenv(
    #     "SQLALCHEMY_DATABASE_URI")


    # db.init_app(app)
    # migrate = Migrate(app, db)
    api = Api(app)

    api.register_blueprint(AvailabilityBluePrint)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
