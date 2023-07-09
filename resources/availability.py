from flask.views import MethodView
from flask_smorest import Blueprint, abort

from schemas import SearchSchema

blp = Blueprint("Expedia", __name__, description="Operations on Expedia")

@blp.route("/availability")
class Availability(MethodView):
    @blp.arguments(SearchSchema)
    def post(self, search_data):
        return {
           "result": search_data
        }