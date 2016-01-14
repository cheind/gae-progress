

import pprint
import argparse
import sys
import urlparse
import time
import inspect

# Requires  Google APIs Client Library
# Install with pip install --upgrade google-api-python-client
from apiclient.discovery import build

def createProgressService(args):
    # Build a service object for interacting with the API.
    apiRoot = urlparse.urljoin(args.url, '_ah/api')
    api = 'progressApi'
    version = 'v1'
    discovery_url = '%s/discovery/v1/apis/%s/%s/rest' % (apiRoot, api, version)
    return build(api, version, discoveryServiceUrl=discovery_url, cache_discovery=False)

def listProgresses(args):
    progress = createProgressService(args)

    result = []
    page_token = None
    param = {
        'order': '-lastUpdated',
        'apikey': args.key
    }

    while True:
        if page_token:
            param['pageToken'] = page_token

        response = progress.list(**param).execute()

        result.extend(response['items'])
        page_token = response.get('nextPageToken')
        if not page_token:
            break

    pprint.pprint(result)

def createProgress(args):
    progress = createProgressService(args)
    response = progress.create(body={'title':args.title, 'description':args.desc, 'apikey':args.key}).execute()
    pprint.pprint(response)

def simulateProgressUpdate(args):
    progress = createProgressService(args)
    param = {'id':args.id, 'apikey':args.key}
    for x in range(0, 100):
        param['progress'] = x
        response = progress.update(body=param).execute()
        print '.',
        time.sleep(0.5)


def main():
     parser = argparse.ArgumentParser(add_help=True)
     subparsers = parser.add_subparsers()

     parserCreateProgress = subparsers.add_parser('create')
     parserCreateProgress.add_argument('--title')
     parserCreateProgress.add_argument('--desc')
     parserCreateProgress.add_argument('--url', default='http://localhost:8080')
     parserCreateProgress.add_argument('--key', required=True)
     parserCreateProgress.set_defaults(func=createProgress)

     parserSimulateProgress = subparsers.add_parser('simulate')
     parserSimulateProgress.add_argument('--id', type=int, required=True)
     parserSimulateProgress.add_argument('--url', default='http://localhost:8080')
     parserSimulateProgress.add_argument('--key', required=True)
     parserSimulateProgress.set_defaults(func=simulateProgressUpdate)

     parserListProgresses = subparsers.add_parser('list')
     parserListProgresses.add_argument('--url', default='http://localhost:8080')
     parserListProgresses.add_argument('--key', required=True)
     parserListProgresses.set_defaults(func=listProgresses)

     args = parser.parse_args()
     args.func(args)

if __name__ == '__main__':
  main()
