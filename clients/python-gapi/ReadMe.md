## Python-gapi client

This console client uses Python and [Google APIs client library](https://developers.google.com/discovery/libraries) to interact with the RESTful `progressApi` service of **gae-progress**.

To run the client you need Python 2.7 and the Google APIs client library for Python. This library can be installed via pip

```
> pip install --upgrade google-api-python-client
```

To use the client you need to supply your API key as command line parameter. An API key is generated automatically for your when you first sign in to the web app of **gae-progress**. You can find and update your API key in the `Profile`.

To create a new progress navigate to `clients/python-gapi` and run
```
> python progress.py create --key YOURAPIKEY --name 'Progress title'
```

When successful you should receive the ID of the newly generated `Progress`

```
{u'id': u'5953992903360512'}
```

By default the client assumes the development server runs at `http://localhost:8080`. For more help on parameters and commands type

```
> python progress.py -h
```
