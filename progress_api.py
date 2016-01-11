
import endpoints
from protorpc import messages
from protorpc import message_types
from protorpc import remote
from google.appengine.ext import ndb
from google.appengine.datastore import datastore_query

from endpoints_proto_datastore.ndb import EndpointsModel
from endpoints_proto_datastore.ndb import EndpointsAliasProperty

import logging
import uuid
import hashlib
from models import *
from utils import ndbAttributesFromString
from pprint import pprint

WEB_CLIENT_ID = '248701908744-ab1in98hrea09g6qe8nrofjsagurm362.apps.googleusercontent.com'
DATETIME_STRING_FORMAT = '%Y-%m-%dT%H:%M:%S.%f'
QUERY_LIMIT_MAX = 100

@endpoints.api(
    name='progressApi',
    version='v1',
    description='Monitor any progress.',
    allowed_client_ids=[WEB_CLIENT_ID, endpoints.API_EXPLORER_CLIENT_ID],
    scopes=[endpoints.EMAIL_SCOPE],)
class ProgressApi(remote.Service):

    @classmethod
    def generateApiKey(cls, hmail):
        return '%s-%s' % (hmail, str(uuid.uuid4()))

    @classmethod
    def splitApiKey(cls, apikey):
        if (apikey is not None):
            parts = apikey.split('-')
            if (len(parts) == 6):
                return parts[0], '-'.join(parts[1:])

    def getUserKeyFromAuth(self):
        cu = endpoints.get_current_user()
        if (cu is not None):
            hmail = hashlib.md5(cu.email()).hexdigest()
            return ndb.Key(User, hmail)

    def getUserKeyFromApiKey(self, apikey):
        if (apikey is not None):
            hmail, verification = ProgressApi.splitApiKey(apikey)
            if (hmail is not None):
                return ndb.Key(User, hmail)

    def getUserFromAuthOrApiKey(self, apikey):
        if (apikey is not None):
            k = self.getUserKeyFromApiKey(apikey)
            if (k is not None):
                u = k.get()
                if (u is not None and u.apikey == apikey):
                    return u
        else:
            k = self.getUserKeyFromAuth()
            if (k is not None):
                return k.get()

    @endpoints.method(
        message_types.VoidMessage,
        UserResponseMessage,
        path='user',
        name='progress.user',
        http_method='GET')
    def getUserProfile(self, request):
        cu = endpoints.get_current_user()
        if (cu is None):
            raise endpoints.UnauthorizedException('Invalid token.')

        hmail = hashlib.md5(cu.email()).hexdigest()
        u_key = ndb.Key(User, hmail)
        u = u_key.get()
        if (u is None):
            u = User(id=hmail, email=cu.email(), apikey=ProgressApi.generateApiKey(hmail))
            u.put()

        return UserResponseMessage(email=u.email, apikey=u.apikey)

    @endpoints.method(
        CreateProgressRequestMessage,
        CreateProgressResponseMessage,
        path='create',
        name='progress.create',
        http_method='POST')
    def createProgress(self, request):
        u = self.getUserFromAuthOrApiKey(request.apikey)
        if (u is None):
            raise endpoints.UnauthorizedException('Not authorized.')

        p = Progress(title=request.title, progress=request.progress, parent=u.key)
        k = p.put()

        return CreateProgressResponseMessage(id=k.id())

    @endpoints.method(
        UpdateProgressRequestMessage,
        message_types.VoidMessage,
        path='update',
        name='progress.update',
        http_method='POST')
    def updateProgress(self, request):
        u = self.getUserFromAuthOrApiKey(request.apikey)
        if (u is None):
            raise endpoints.UnauthorizedException('Not authorized.')

        p = Progress.get_by_id(request.id, parent=u.key)
        if (p is None):
            raise endpoints.NotFoundException('Progress with id %i not found' % request.id)

        p.progress = request.progress or p.progress
        p.title = request.title or p.title
        p.put()

        return message_types.VoidMessage()

    @endpoints.method(
        QueryProgressRequestMessage,
        QueryProgressResponseMessage,
        path='list',
        name='progress.list',
        http_method='GET')
    def queryProgresses(self, request):
        u = self.getUserFromAuthOrApiKey(None)
        if (u is None):
            raise endpoints.UnauthorizedException('Not authorized.')

        q = Progress.query(ancestor=u.key)
        orderAttr = ndbAttributesFromString(request.order, Progress)
        logging.info("Order: %s" % orderAttr)
        if (orderAttr is not None):
            q = q.order(*orderAttr)


        qopts = {}
        if (request.pageToken is not None):
            cursor = datastore_query.Cursor.from_websafe_string(request.pageToken)
            qopts['start_cursor'] = cursor

        limit = request.limit or 10
        limit = max(1, min(limit, QUERY_LIMIT_MAX))
        items, cursor, moreResults = q.fetch_page(limit, **qopts)
        if not moreResults:
          cursor = None

        ps = []
        for pm in items:
            prm = ProgressResponseMesssage(
                id=pm.key.id(),
                title=pm.title,
                progress=pm.progress,
                created=pm.created.strftime(DATETIME_STRING_FORMAT),
                lastUpdated=pm.lastUpdated.strftime(DATETIME_STRING_FORMAT))
            ps.append(prm)

        thisToken = request.pageToken
        nextToken = cursor.to_websafe_string() if cursor else None
        prevToken = cursor.reversed().to_websafe_string() if cursor else None
        return QueryProgressResponseMessage(items=ps, thisPageToken=thisToken, nextPageToken=nextToken, prevPageToken=None)

APPLICATION = endpoints.api_server([ProgressApi], restricted=False)
