

import pprint
import argparse
import sys
import urlparse
import time
import inspect

# Requires  Google APIs Client Library
# Install with pip install --upgrade google-api-python-client
from apiclient.discovery import build

def createService(args):
    # Build a service object for interacting with the API.
    apiRoot = urlparse.urljoin(args.url, '_ah/api')
    api = 'progressApi'
    version = 'v1'
    discovery_url = '%s/discovery/v1/apis/%s/%s/rest' % (apiRoot, api, version)
    return build(api, version, discoveryServiceUrl=discovery_url, cache_discovery=False)

def listProgresses(args):
    service = createService(args)

    result = []
    page_token = None
    param = {}
    param['order'] = '-created'
    while True:
        if page_token:
            param['pageToken'] = page_token

        response = service.progress().list(**param).execute()

        result.extend(response['items'])
        page_token = response.get('nextPageToken')
        if not page_token:
            break

    pprint.pprint(result)

def createProgress(args):
    service = createService(args)
    response = service.progress().create(body={'title':args.name, 'description':args.desc, 'apikey':args.key}).execute()
    pprint.pprint(response)

def simulateProgressUpdate(args):
    service = createService(args)
    param = {'id':args.id, 'apikey':args.key}
    for x in range(0, 100):
        param['progress'] = x
        response = service.progress().update(body=param).execute()
        print '.',
        time.sleep(0.5)


def main():
     parser = argparse.ArgumentParser(add_help=True)
     subparsers = parser.add_subparsers()

     parserCreateProgress = subparsers.add_parser('create')
     parserCreateProgress.add_argument('--name')
     parserCreateProgress.add_argument('--desc')
     parserCreateProgress.add_argument('--url', default='http://localhost:8080')
     parserCreateProgress.add_argument('--key', required=True)
     parserCreateProgress.set_defaults(func=createProgress)

     parserSimulateProgress = subparsers.add_parser('simulate')
     parserSimulateProgress.add_argument('--id', type=int, required=True)
     parserSimulateProgress.add_argument('--url', default='http://localhost:8080')
     parserSimulateProgress.add_argument('--key', required=True)
     parserSimulateProgress.set_defaults(func=simulateProgressUpdate)

     parserSimulateProgress = subparsers.add_parser('list')
     parserSimulateProgress.add_argument('--url', default='http://localhost:8080')
     parserSimulateProgress.add_argument('--key', required=True)
     parserSimulateProgress.set_defaults(func=listProgresses)

     args = parser.parse_args()
     args.func(args)

if __name__ == '__main__':
  main()
