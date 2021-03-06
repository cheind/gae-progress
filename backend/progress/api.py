
import endpoints
from protorpc import messages
from protorpc import message_types
from protorpc import remote
from google.appengine.ext import ndb
from google.appengine.datastore import datastore_query

import uuid
import hashlib

import models
import constants
import utils

@endpoints.api(
    name='progressApi',
    version='v1',
    description='Manage any progress.',
    allowed_client_ids=constants.CLIENT_IDS,
    scopes=[endpoints.EMAIL_SCOPE],)
class ProgressApi(remote.Service):
    """Remote service providing methods to manage progresses."""

    def generateApiKey(self, hmail):
        """Generate an API key from hashed E-Mail and UUID."""
        return '%s-%s' % (hmail, str(uuid.uuid4()))

    def splitApiKey(self, apikey):
        """Retrieve the hashed E-Mail part from the API key.

        Returns:
            Hashed E-Mail if successful, None otherwise.
        """
        if (apikey is not None):
            parts = apikey.split('-')
            if (len(parts) == 6):
                return parts[0]

    def getUserFromApiKey(self, apikey):
        """Retrieve User from API key.

        Returns:
            User from datastore if successful, None otherwise.
        """
        if (apikey is not None):
            hmail = self.splitApiKey(apikey)
            if (hmail is not None):
                return ndb.Key(models.User, hmail).get()

    def getUser(self, apikey=None, createNew=True):
        """Get or create User.

        This method supports 2 ways of authenticating users. First via
        API keys and second via OAuth2. When using OAuth2 this method is
        able to create new users on the fly.

        Args:
            apikey: When specified User is searched by API key authentication.
            createNew: Whether or not to implicitely create a new user when Authenticated
                       via OAuth2.

        Returns:
            User from datastore if successful, None otherwise.
        """
        u = None
        if (apikey is not None):
            u = self.getUserFromApiKey(apikey)
            if (u is not None and u.apikey != apikey):
                u = None
        else:
            cu = endpoints.get_current_user()
            if (cu is not None):
                hmail = hashlib.md5(cu.email()).hexdigest()
                k = ndb.Key(models.User, hmail)
                u = k.get()
                if (u is None and createNew):
                    u = models.User(id=hmail, email=cu.email(), apikey=self.generateApiKey(hmail))
                    u.put()
        return u

    def clampProgress(self, value):
        """Clamp value to [0..100] range."""
        if (value is not None):
            return max(0.0, min(value, 100.0))

    @endpoints.method(
        message_types.VoidMessage,
        models.UserResponseMessage,
        path='userProfile',
        name='userProfile',
        http_method='GET')
    def getUserProfile(self, request):
        """Remote method to retrieve the user profile of current user."""
        u = self.getUser()
        if (u is None):
            raise endpoints.UnauthorizedException('Not authorized.')

        return models.UserResponseMessage(email=u.email, apikey=u.apikey)

    @endpoints.method(
        message_types.VoidMessage,
        models.UserResponseMessage,
        path='generateNewApiKey',
        name='generateNewApiKey',
        http_method='GET')
    def generateNewApiKey(self, request):
        """Remote method to generate a new API key for current user."""
        u = self.getUser()

        if (u is None):
            raise endpoints.UnauthorizedException('Not authorized.')

        u.apikey = self.generateApiKey(u.key.id())
        u.put()

        return models.UserResponseMessage(email=u.email, apikey=u.apikey)

    @endpoints.method(
        models.CreateProgressRequestMessage,
        models.CreateProgressResponseMessage,
        path='create',
        name='create',
        http_method='POST')
    def createProgress(self, request):
        """Remote method to create a new progress."""
        u = self.getUser(apikey=request.apikey)

        if (u is None):
            raise endpoints.UnauthorizedException('Not authorized.')

        p = models.Progress(
            title=request.title,
            description=request.description,
            progress=self.clampProgress(request.progress),
            parent=u.key)

        k = p.put()

        return models.CreateProgressResponseMessage(id=k.id())

    @endpoints.method(
        models.UpdateProgressRequestMessage,
        message_types.VoidMessage,
        path='update',
        name='update',
        http_method='POST')
    def updateProgress(self, request):
        """Remote method to update an existing progress."""
        u = self.getUser(apikey=request.apikey)

        if (u is None):
            raise endpoints.UnauthorizedException('Not authorized.')

        # Need to specify parent, as id is only unique in combination with
        # a parent key
        p = models.Progress.get_by_id(request.id, parent=u.key)
        if (p is None):
            raise endpoints.NotFoundException('Progress with id %i not found' % request.id)

        p.description = request.description or p.description
        p.title = request.title or p.title
        p.progress = self.clampProgress(request.progress) or p.progress
        p.put()

        return message_types.VoidMessage()

    @endpoints.method(
        models.DeleteProgressRequestMessage,
        message_types.VoidMessage,
        path='delete',
        name='delete',
        http_method='POST')
    def deleteProgress(self, request):
        """Remote method delete an existing progress."""
        u = self.getUser(apikey=request.apikey)

        if (u is None):
            raise endpoints.UnauthorizedException('Not authorized.')

        k = ndb.Key(models.Progress, request.id, parent=u.key)
        k.delete()

        return message_types.VoidMessage()

    @endpoints.method(
        models.QueryProgressRequestMessage,
        models.QueryProgressResponseMessage,
        path='list',
        name='list',
        http_method='GET')
    def queryProgresses(self, request):
        """Remote method query progresses.

        This methods supports pagination and custom orders.
        """
        u = self.getUser(apikey=request.apikey)

        if (u is None):
            raise endpoints.UnauthorizedException('Not authorized.')

        # Query progresses created by current user.
        q = models.Progress.query(ancestor=u.key)

        # Infer ordering from stringified attribute names.
        orderAttr = utils.ndbAttributesFromString(request.order, models.Progress)
        if (orderAttr is not None):
            q = q.order(*orderAttr)

        # When a page token is supplied, use it to initialize the cursor.
        qopts = {}
        if (request.pageToken is not None):
            cursor = datastore_query.Cursor.from_websafe_string(request.pageToken)
            qopts['start_cursor'] = cursor


        limit = request.limit or 10
        limit = max(1, min(limit, constants.QUERY_LIMIT_MAX))

        # Execute query.
        items, cursor, moreResults = q.fetch_page(limit, **qopts)
        if not moreResults:
          cursor = None

        # Assemble result message.
        # Be aware: although id modelled as IntegerField, it is being serialized as
        # string. See https://code.google.com/p/googleappengine/issues/detail?id=9173
        # for details.
        ps = []
        for pm in items:
            prm = models.ProgressResponseMessage(
                id=pm.key.id(),
                title=pm.title,
                description=pm.description,
                progress=pm.progress,
                created=pm.created.strftime(constants.DATETIME_STRING_FORMAT),
                lastUpdated=pm.lastUpdated.strftime(constants.DATETIME_STRING_FORMAT))
            ps.append(prm)

        # If there are more pages to be queried, make sure to include a page token in
        # the result.
        nextToken = cursor.to_websafe_string() if cursor else None
        return models.QueryProgressResponseMessage(items=ps, nextPageToken=nextToken, thisPageToken=request.pageToken)
