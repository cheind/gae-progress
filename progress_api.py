
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
                return parts[0]

    def getUserFromApiKey(self, apikey):
        if (apikey is not None):
            hmail = ProgressApi.splitApiKey(apikey)
            if (hmail is not None):
                return ndb.Key(User, hmail).get()

    def getUser(self, apikey=None, createNew=True):
        u = None
        if (apikey is not None):
            u = self.getUserFromApiKey(apikey)
            if (u is not None and u.apikey != apikey):
                u = None
        else:
            cu = endpoints.get_current_user()
            if (cu is not None):
                hmail = hashlib.md5(cu.email()).hexdigest()
                k = ndb.Key(User, hmail)
                u = k.get()
                if (u is None and createNew):
                    u = User(id=hmail, email=cu.email(), apikey=ProgressApi.generateApiKey(hmail))
                    u.put()
        return u

    @endpoints.method(
        message_types.VoidMessage,
        UserResponseMessage,
        path='user',
        name='progress.user',
        http_method='GET')
    def getUserProfile(self, request):
        u = self.getUser()
        if (u is None):
            raise endpoints.UnauthorizedException('Not authorized.')

        return UserResponseMessage(email=u.email, apikey=u.apikey)

    @endpoints.method(
        message_types.VoidMessage,
        UserResponseMessage,
        path='generateNewApiKey',
        name='progress.generateNewApiKey',
        http_method='GET')
    def generateNewApiKey(self, request):
        u = self.getUser()

        if (u is None):
            raise endpoints.UnauthorizedException('Not authorized.')

        u.apikey = ProgressApi.generateApiKey(u.key.id())
        u.put()

        return UserResponseMessage(email=u.email, apikey=u.apikey)

    @endpoints.method(
        CreateProgressRequestMessage,
        CreateProgressResponseMessage,
        path='create',
        name='progress.create',
        http_method='POST')
    def createProgress(self, request):
        u = self.getUser(apikey=request.apikey)

        if (u is None):
            raise endpoints.UnauthorizedException('Not authorized.')

        p = Progress(
            title=request.title,
            description=request.description,
            progress=request.progress,
            parent=u.key)

        k = p.put()

        return CreateProgressResponseMessage(id=k.id())

    @endpoints.method(
        UpdateProgressRequestMessage,
        message_types.VoidMessage,
        path='update',
        name='progress.update',
        http_method='POST')
    def updateProgress(self, request):
        u = self.getUser(apikey=request.apikey)

        if (u is None):
            raise endpoints.UnauthorizedException('Not authorized.')

        # Need to specify parent, as id is only unique in combination with
        # a parent key
        p = Progress.get_by_id(request.id, parent=u.key)
        if (p is None):
            raise endpoints.NotFoundException('Progress with id %i not found' % request.id)

        p.description = request.description or p.description
        p.title = request.title or p.title
        p.progress = request.progress or p.progress
        p.put()

        return message_types.VoidMessage()

    @endpoints.method(
        QueryProgressRequestMessage,
        QueryProgressResponseMessage,
        path='list',
        name='progress.list',
        http_method='GET')
    def queryProgresses(self, request):
        u = self.getUser(apikey=request.apikey)

        if (u is None):
            raise endpoints.UnauthorizedException('Not authorized.')

        q = Progress.query(ancestor=u.key)
        orderAttr = ndbAttributesFromString(request.order, Progress)
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
                description=pm.description,
                progress=pm.progress,
                created=pm.created.strftime(DATETIME_STRING_FORMAT),
                lastUpdated=pm.lastUpdated.strftime(DATETIME_STRING_FORMAT))
            ps.append(prm)

        thisToken = request.pageToken
        nextToken = cursor.to_websafe_string() if cursor else None
        prevToken = cursor.reversed().to_websafe_string() if cursor else None
        return QueryProgressResponseMessage(items=ps, thisPageToken=thisToken, nextPageToken=nextToken, prevPageToken=None)

APPLICATION = endpoints.api_server([ProgressApi], restricted=False)
