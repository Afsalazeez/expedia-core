from flask.views import MethodView
from flask_smorest import Blueprint, abort
from passlib.hash import pbkdf2_sha256

from sqlalchemy.exc import SQLAlchemyError

from schemas import UserSchema
from models import UserModel

from db import db

blp = Blueprint("users", __name__, description="Operations on Users")

@blp.route("/user/<int:user_id>")
class User(MethodView):
    @blp.response(200, UserSchema)
    def get(self, user_id):
        return {
            "id" : user_id,
            "username": "test",
            "email": "test@test.com",
        }
    

@blp.route("/user")
class UserList(MethodView):
    @blp.arguments(UserSchema)
    @blp.response(200, UserSchema)
    def post(self, user_data):
        if UserModel.query.filter(
            UserModel.username == user_data['username'],
            UserModel.email == user_data["email"]
        ).first():
            abort(
                409,
                message="A user with that email/username already exists"
            )

        try:

            user = UserModel(
                username=user_data["username"],
                email=user_data["email"],
                password=pbkdf2_sha256.hash(user_data["password"])
            )

            db.session.add(user)
            db.session.commit()

            # send_push_email.delay(user.email, user.username)

        except SQLAlchemyError:
            abort(
                500,
                message="An error occured while creating new user"
            )
        return user, 201