## Web application

This folder is a placeholder for the web application client of **gae-progress**. The web app is actually served by the server instance and code can be found in [`backend/www`](../../backend/www).

The web app runs in the clients browser. Web pages are served from the development / live server. These pages are static but contain [AngularJS](https://angularjs.org/) logic that is being evaluated on the client side. This logic accesses the `progressApi` through  [Google APIs client library](https://developers.google.com/discovery/libraries) in JavaScript.

The web app supports full user management and progress management. Note that `progressApi` creates new users only from OpenID Connect authentication. Before using any other client you need sign in once using the web app.

Try the [live demo](https://progress-1181.appspot.com).
