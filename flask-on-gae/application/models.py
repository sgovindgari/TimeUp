from google.appengine.ext import db
import datetime
import decimal

class DecimalProperty(db.Property):
    data_type=decimal.Decimal

    def get_value_for_datastore(self, model_instance):
        return str(super(DecimalProperty, self).get_value_for_datastore(model_instance))

    def make_value_from_datastore(self, value):
        return decimal.Decimal(str(value))

    def validate(self, value):
        value = super(DecimalProperty, self).validate(value)
        if value is None:
            return decimal.Decimal(str(0.00))
        elif isinstance(value, decimal.Decimal):
            return value
        elif isinstance(value, basestring):
            return decimal.Decimal(value)
        raise db.BadValueError("Property %s must be a Decimal or string." % self.name)

class User(db.Model):
    username = db.StringProperty(required = True)
    email = db.EmailProperty()
    passwd = db.StringProperty(required = True)
    f_name = db.StringProperty(required = True)
    l_name = db.StringProperty(required = True)
    mpg = db.FloatProperty(default = 20.0)
    transit_cost = db.FloatProperty(default = 2.0)

    # Preferences
    driving = db.BooleanProperty(default = True)
    walking = db.BooleanProperty(default = True)
    transit = db.BooleanProperty(default = True)
    time_added = db.DateTimeProperty(auto_now_add=True)
    carbon = db.FloatProperty(default = 0.0)
    savings = db.FloatProperty(default = 0.00)
    metric = db.StringProperty(choices=set(['k','m']), default = 'k')
    rec_loc = db.StringListProperty()
    fav_loc = db.StringListProperty()

class Loc(db.Model):
    address = db.StringProperty(required = True)

class FavLoc(Loc):
    name = db.StringProperty(required = True)

