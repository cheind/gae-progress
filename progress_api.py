import endpoints
from protorpc import remote
from google.appengine.ext import ndb
from endpoints_proto_datastore.ndb import EndpointsModel

class Progress(EndpointsModel):
    _message_fields_schema = ('id', 'title', 'progress', 'created')
    title = ndb.StringProperty(default='Untitled progress')
    progress = ndb.FloatProperty(default=0.0)
    created = ndb.DateTimeProperty(auto_now_add=True)

@endpoints.api(name='progressApi', version='v1', description='Monitor any progress.')
class ProgressApi(remote.Service):

    @Progress.method(path='create', http_method='POST', name='progress.create')
    def createProgress(self, my_progress):
        my_progress.put()
        return my_progress

    @Progress.method(path='update', http_method='POST', name='progress.update')
    def updateProgress(self, my_progress):
        if not my_progress.from_datastore:
            my_id = my_progress.id
            raise endpoints.BadRequestException('Progress %d does not exists.' % (my_id,))

        my_progress.put()
        return my_progress


APPLICATION = endpoints.api_server([ProgressApi], restricted=False)
