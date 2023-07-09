from datetime import datetime, date
import json
from marshmallow import Schema, fields, validates, validates_schema, ValidationError

from static.counties import COUNTRIES

class RoomSchema(Schema):
    adults = fields.Integer( required=True)
    children = fields.List(fields.Integer(), required=True)

    @validates('children')
    def validate_children(self, children):
        for child in children:
            if not 0 <= child <= 12:
                raise ValidationError("The child age should be between 0 - 12 ")
        if len(children) > 4:
            raise ValidationError("The maximum number of children in a room is 4.")


    @validates('adults')
    def validate_occupancy(self, adults):
        if adults > 4:
            raise ValidationError("The maximum number of adults in a room is 4")

    @validates_schema
    def validate_room(self, data, **kwargs):
        adults = data.get('adults')
        children = data.get('children')

        if len(children) + adults > 4:
            raise ValidationError("The maximum occupancy of the room combined with adults and children is 4")



class PreferencesSchema(Schema):
    nationality = fields.Str(required=True)
    checkin = fields.Str(required=True)
    currency = fields.Str(required=True)
    nights = fields.Integer(required=True)
    
    @validates('checkin')
    def validate_checkin(self, checkin):
        parsed_date = None

        try: 
            parsed_date = datetime.strptime(checkin, "%Y-%m-%d")

        except:
            raise ValidationError("Invalid check-in date format. Expected format YYYY-MM-DD")


        if parsed_date < datetime.today():
            raise ValidationError("The check-in date must be in the future")

    @validates('currency')
    def validate_currency(self, currency):
        if currency not in COUNTRIES.values():
            raise ValidationError("Invalid Currency. Check the list of valid Currencies from the static API")

    @validates('nationality')
    def validate_nationality(self, nationality):
        if nationality not in COUNTRIES.keys():
            raise ValidationError("Invalid nationality. Check the list of valid Nationalities from the static API")
        
    @validates_schema
    def validate_schema(self, data, **kwargs):
        nationality = data.get('nationality')
        currency = data.get('currency')

        if COUNTRIES[nationality] != currency:
            raise ValidationError("Nationality and currency doesn't match")
        



class SearchSchema(Schema):
    hotel_codes = fields.List(fields.Integer(), required=True)
    preferences = fields.Nested(PreferencesSchema, required=True)
    rooms = fields.List(fields.Nested(RoomSchema), required=True)

    @validates('hotel_codes')
    def validate_hotel_codes(self, hotel_codes):
        if len(hotel_codes) < 1:
            raise ValidationError("Fields rooms must not be empty")

    @validates('rooms')
    def validate_rooms(self, rooms):
        if len(rooms) < 1:
            raise ValidationError("Fields rooms must not be empty")



