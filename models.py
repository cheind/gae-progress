
from protorpc import messages
from google.appengine.ext import ndb

class User(ndb.Model):
    email = ndb.StringProperty()
    apikey = ndb.StringProperty()

class UserResponseMessage(messages.Message):
    email = messages.StringField(1);
    apikey = messages.StringField(2);
