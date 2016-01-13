## What it does
**gae-progress** is a [Google App Engine](https://cloud.google.com/appengine/) (GAE) project managing arbitrary progresses. It is meant for people getting started with GAE and [PaaS](https://en.wikipedia.org/wiki/Platform_as_a_service).
![Web Client](etc/webfront.png)

Test the [live demo](https://progress-1181.appspot.com).

## What's in it

The features at a glance:
  - Create, update, delete and query progresses.
  - User authentication / authorization using [OpenID Connect](https://developers.google.com/identity/protocols/OpenIDConnect) or alternatively using API keys.
  - Query pagination using cursors.
  - Clients using [Google APIs client library](https://developers.google.com/discovery/libraries) (Python, Javascript and Java).

## Structure

The project is structured as follows:
  - the `backend` directory contains files making up the application that runs on GAE. It consists of
    - `backend/progress` a RESTful API for managing progresses based [Google Endpoints API](https://cloud.google.com/appengine/docs/python/endpoints/)
    - `backend/www` a set of static webpages served to rich web clients
  - the `clients` directory contains additional clients utilizing the progress API.

## Running the backend service

A couple of steps are required in order to run this service under your Google account.

  1. Fork or download this repository.
  1. Create a new project using [Google Developer Console](https://console.developers.google.com) and write down its `Project-ID`.
  1. Create new credentials for OAuth (OpenID connect) support. More info on this process can be found [here](https://cloud.google.com/appengine/docs/python/endpoints/auth#Python_Creating_OAuth_20_client_IDs).
    1. In the developer console navigate open *API Manager/Credentials* and create a new *OAuth client ID* credential.
    1. Select *Web application*.
    1. In *Authorized Javascript Origins* add `http://localhost:8080` and `https://<Project-ID>.appspot.com`.
    1. In *Authorized redirect URIs* add `http://localhost:8080/oauth2callback` and `https://<Project-ID>.appspot.com/oauth2callback`.
    1. Write down the generated `Client-ID`.
    1. In *API Manager/Credentials* create a *OAuth Consent Screen*. Default values are ok.
  1. In `backend/app.yaml` update `application: <Project-ID>`
  1. In `backend/progress/constants.py` update `WEB_CLIENT_ID = '<Client-ID>'`
  1. In `backend/www/js/app.js` update `CLIENT_ID: '<Client-ID>'`
  1. Install the [Google App Engine SDK for Python](https://cloud.google.com/appengine/downloads#Google_App_Engine_SDK_for_Python). At the time of writing the 1.9.30 was the most recent version.

To run development server locally invoke

```
> devappserver.py .
```

from your `backend` directory. If all goes well you should be able to access `http://localhost:8080` and see welcome message similar to:

![Web Client](etc/welcome.png)

If you cannot access the service, make you don't spot any errors in the console log. If you have multiple GAE instances running locally, check which port was bound by the server. Browsing the logs you should see something along the lines of:
```
Starting module "default" running at: http://localhost:8080
```
