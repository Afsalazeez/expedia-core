from marshmallow import Schema, fields, validate, ValidationError

class UserSchema(Schema):
    id = fields.Integer(dump_only=True)
    username = fields.Str(required=True)
    email = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)


class RoomSchema(Schema):
    adults = fields.Integer( required=True)
    children = fields.List(fields.Integer(), required=True)

    @validate('children')
    def validate_children(self, children):
        for child in children:
            if not 1 <= child <= 12:
                raise ValidationError("The child age should be between 1 - 12 ")


    @validate('adults')
    def validate_occupancy(self, adults):
        children_count = len(self.context['children'])
        


class PreferencesSchema(Schema):
    nationality = fields.Str(required=True)
    checkin = fields.Str(required=True)
    currency = fields.Str(required=True)
    nights = fields.Integer(required=True)
    rooms = fields.Nest(RoomSchema)

class SearchSchema(Schema):
    hotel_codes = fields.List(fields.Integer(), required=True)
    preferecens = fields.Nested(PreferencesSchema)


