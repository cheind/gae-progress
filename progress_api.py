import endpoints
from protorpc import remote
from google.appengine.ext import ndb
from endpoints_proto_datastore.ndb import EndpointsModel
from endpoints_proto_datastore.ndb import EndpointsAliasProperty
import uuid

WEB_CLIENT_ID = '248701908744-ab1in98hrea09g6qe8nrofjsagurm362.apps.googleusercontent.com'


class Progress(EndpointsModel):
    _message_fields_schema = ('id', 'title', 'progress', 'created')
    title = ndb.StringProperty(default='Untitled progress')
    progress = ndb.FloatProperty(default=0.0)
    created = ndb.DateTimeProperty(auto_now_add=True)

    DEFAULT_ORDER = '-created'
    @EndpointsAliasProperty(setter=EndpointsModel.OrderSet, default=DEFAULT_ORDER)
    def order(self):
        return super(Progress, self).order

class User(EndpointsModel):
    profile = ndb.UserProperty()
    apikey = ndb.StringProperty()

@endpoints.api(
    name='progressApi',
    version='v1',
    description='Monitor any progress.',
    allowed_client_ids=[WEB_CLIENT_ID, endpoints.API_EXPLORER_CLIENT_ID],
    scopes=[endpoints.EMAIL_SCOPE],)
class ProgressApi(remote.Service):

    @Progress.method(path='create', http_method='POST', name='progress.create', request_fields=('title', 'progress'), response_fields=('id',))
    def createProgress(self, my_progress):
        my_progress.put()
        return my_progress

    @Progress.method(
        path='update',
        http_method='POST',
        name='progress.update',)
    def updateProgress(self, my_progress):
        if not my_progress.from_datastore:
            my_id = my_progress.id
            raise endpoints.BadRequestException('Progress %d does not exists.' % (my_id,))

        my_progress.put()
        return my_progress

    @Progress.query_method(path='list', name='progress.list', query_fields=('order', 'limit', 'pageToken',), collection_fields=('id', 'title', 'progress', 'created'), http_method='GET')
    def listProgress(self, query):
        return query

    @Progress.method(path='get/{id}', name='progress.get', request_fields=('id',), http_method='GET')
    def getProgress(self, my_progress):
        if not my_progress.from_datastore:
            raise endpoints.NotFoundException('Progress not found.')
        return my_progress

    @User.method(path='user', name='progress.user', user_required=True)
    def getUser(self, my_user):
        my_user.profile = endpoints.get_current_user()

        if not my_user.from_datastore:
            my_user.apikey = str(uuid.uuid4())

        my_user.put()
        return my_user

APPLICATION = endpoints.api_server([ProgressApi], restricted=False)
