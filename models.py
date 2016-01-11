
from protorpc import messages
from google.appengine.ext import ndb

class User(ndb.Model):
    email = ndb.StringProperty()
    apikey = ndb.StringProperty()

class UserResponseMessage(messages.Message):
    email = messages.StringField(1)
    apikey = messages.StringField(2)

class Progress(ndb.Model):
    title = ndb.StringProperty(default='Untitled progress')
    progress = ndb.FloatProperty(default=0.0)
    created = ndb.DateTimeProperty(auto_now_add=True)
    lastUpdated = ndb.DateTimeProperty(auto_now=True)

class CreateProgressRequestMessage(messages.Message):
    title = messages.StringField(1, default='Untitled progress')
    progress = messages.FloatField(2, default=0.0)
    apikey = messages.StringField(3)

class CreateProgressResponseMessage(messages.Message):
    id = messages.IntegerField(1)

class ProgressResponseMesssage(messages.Message):
    id = messages.IntegerField(1)
    title = messages.StringField(2)
    progress = messages.FloatField(3)
    created = messages.StringField(4)
    lastUpdated = messages.StringField(5)

class QueryProgressRequestMessage(messages.Message):
    limit = messages.IntegerField(1, default=10)
    order = messages.StringField(2, default='-created')
    pageToken = messages.StringField(3)

class QueryProgressResponseMessage(messages.Message):
    items = messages.MessageField(ProgressResponseMesssage, 1, repeated=True)
    thisPageToken = messages.StringField(2)
    prevPageToken = messages.StringField(3)
    nextPageToken = messages.StringField(4)

class UpdateProgressRequestMessage(messages.Message):
    id = messages.IntegerField(1, required=True)
    title = messages.StringField(2)
    progress = messages.FloatField(3)
    apikey = messages.StringField(4)
