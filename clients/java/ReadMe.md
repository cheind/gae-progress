## Java client

This console client uses Java to interact with the RESTful `progressApi` service of **gae-progress**.

#### Generating library API bundle

Use the [Google Endpoints Tool](https://cloud.google.com/appengine/docs/python/endpoints/endpoints_tool) to generate a Java client library bundle. Switch to the `backend` directory and invoke

```
> endpointscfg.py get_client_lib java -bs default progress.api.ProgressApi
```

This will generate a file called `progressApi-v1.zip` containing the necessary source files and dependencies. Alternatively, you can generate bundles for [Maven](https://maven.apache.org/) or [Gradle](http://gradle.org) as described in the docs.

Generation has already been done for you. The necessary files have been placed in `src/com`,
and `libs`directory.

#### Running the application

Assuming that you have exported the build as runnable jar, you can invoke it as

```
>java -jar progress.jar -command list -key YOUR-API-KEY -url http://localhost:8080
```

to fetch a list of your progresses. If all goes well you should see something along the lines of

```
{
  "created": "2016-01-15T09:35:47.075000Z",
  "description": "No description provided",
  "id": "5184609641824256",
  "lastUpdated": "2016-01-15T09:35:47.075000Z",
  "progress": 0.0,
  "title": "Preparing Lunch"
}
```
