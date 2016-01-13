import endpoints

WEB_CLIENT_ID = '248701908744-ab1in98hrea09g6qe8nrofjsagurm362.apps.googleusercontent.com'
CLIENT_IDS = [WEB_CLIENT_ID, endpoints.API_EXPLORER_CLIENT_ID]

# Python datetime.isoformat seems not to include timezone information, therefore we
# explicitly specify a format string with a trailing Z for UTC time
DATETIME_STRING_FORMAT = '%Y-%m-%dT%H:%M:%S.%fZ'

QUERY_LIMIT_MAX = 100
