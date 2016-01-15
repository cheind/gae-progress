import endpoints

WEB_CLIENT_ID = '248701908744-ab1in98hrea09g6qe8nrofjsagurm362.apps.googleusercontent.com'
"""Allowed web client to access ProgressApi via OAuth2.

You need to change this value to your own client ids as documented at
https://github.com/cheind/gae-progress/
"""

CLIENT_IDS = [WEB_CLIENT_ID, endpoints.API_EXPLORER_CLIENT_ID]
"""Set of allowed clients to access ProgressApi via OAuth2."""

DATETIME_STRING_FORMAT = '%Y-%m-%dT%H:%M:%S.%fZ'
"""Custom date-time format.

Python datetime.isoformat seems not to include timezone information, therefore
we explicitly specify a format string with a trailing Z for UTC time
"""

QUERY_LIMIT_MAX = 100
"""Max number of query results per page."""
