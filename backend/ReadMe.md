## Backend services

This is folder contains the backend services provided by [gae-progress](../../Readme.md). The backend services consist of a RESTful web service named `progressApi` to manage progresses and a web server to serve a set of static web pages.

A couple of steps are required in order to run this backend service under your Google account.

#### Create a new GAE project

Open the [Google Developer Console](https://console.developers.google.com), click on *Create a project* and write down its `Project-ID`.

#### Set up credentials

Next, you need to create new credentials for OAuth (OpenID connect) support. This will be needed so users can authenticate with our progress API via the web app. Here are the steps.

  1. In the developer console open *API Manager/Credentials* and create a new *OAuth client ID* credential.
  1. Select *Web application*.
  1. In *Authorized Javascript Origins* add `http://localhost:8080` and `https://Project-ID.appspot.com`.
  1. In *Authorized redirect URIs* add `http://localhost:8080/oauth2callback` and `https://Project-ID.appspot.com/oauth2callback`.
  1. Write down the generated `Client-ID`.
  1. In *API Manager/Credentials* create a *OAuth Consent Screen*. Default values are ok.

If you are feeling lost, more info on this process can be found [here](https://cloud.google.com/appengine/docs/python/endpoints/auth#Python_Creating_OAuth_20_client_IDs).

#### Get the source code
Fork or download a [release](/releases) of this repository. Update the source using your `Client-ID` and `Project-ID` values.

  - In `backend/app.yaml` update `application: Project-ID`
  - In `backend/progress/constants.py` update `WEB_CLIENT_ID = 'Client-ID'`
  - In `backend/www/js/app.js` update `CLIENT_ID: 'Client-ID'`

#### Start the development server

Install the [Google App Engine SDK for Python](https://cloud.google.com/appengine/downloads#Google_App_Engine_SDK_for_Python). At the time of writing the 1.9.30 was the most recent version. Navigate to the `backend` directory and run

```
> devappserver.py .
```

from the command line. If all goes well you should be able to access `http://localhost:8080` and see welcome message similar to:

![Web Client](../etc/welcome.png)

If you cannot access the service, make you don't spot any errors in the console log. If you have multiple GAE instances running locally, check which port was bound by the server. Browsing the output you should see something along the lines of:
```
Starting module "default" running at: http://localhost:8080
```

## RESTful API

Head over to [progress](./progress/) to browse the documentation for the `progressApi`.

## Web app

Head over to [progress](./www) to browse the documentation for the web app.
