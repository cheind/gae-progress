## Web application

This folder is a placeholder for the web application client of **gae-progress**. The web app is actually served by the server instance and code can be found in [`backend/www`](../../backend/www).

The web app runs in the client browser. Web pages are served from the development / live server. These pages are static but contain [AngularJS](https://angularjs.org/) logic that is being evaluated on the client side. This logic accesses the `progressApi` through  [Google APIs client library](https://developers.google.com/discovery/libraries) in JavaScript.

The web app supports full user management and progress management. Note that `progressApi` creates new users only from OpenID Connect authentication.

**Note** Before using any API key based client you need sign in once using the web app to have your key generated.

Try the [live demo](https://progress-1181.appspot.com).
