
'use strict';

var progressApp = angular.module('ProgressApp', ['ngRoute'])

progressApp.config(function($routeProvider, $locationProvider) {
  $routeProvider.
    when('/profile', {
      templateUrl: '/views/profile.html',
      controller: 'ProfileCtrl'
    }).
    when('/', {
      templateUrl: '/views/home.html',
      controller: 'HomeCtrl'
    }).
    otherwise('/');

    $locationProvider.html5Mode(true);
})

progressApp.factory('oauth2Provider', function() {

  var oauth2Provider = {
    CLIENT_ID: '248701908744-ab1in98hrea09g6qe8nrofjsagurm362.apps.googleusercontent.com',
    SCOPES: 'https://www.googleapis.com/auth/userinfo.email profile',
  };

  oauth2Provider.signIn = function(immediate, authCallback) {
    gapi.auth.authorize({
      'client_id': oauth2Provider.CLIENT_ID,
      'scope': oauth2Provider.SCOPES,
      'immediate': immediate,
      cookie_policy: 'single_host_origin'
    },
    authCallback);
  }

  oauth2Provider.signOut = function() {
    var revokeUrl = 'https://accounts.google.com/o/oauth2/revoke?token=' + gapi.auth.getToken().access_token;
    $.ajax({
      type: 'GET',
      url: revokeUrl,
      async: false,
      contentType: "application/json",
      dataType: 'jsonp',
      success: function(nullResponse) {
        console.log('disconnected');
        // Do something now that user is disconnected
        // The response is always undefined.
      },
      error: function(e) {
        console.log('failed');
        // Handle the error
        // console.log(e);
        // You could point users to manually disconnect if unsuccessful
        // https://plus.google.com/apps
      }
    });
  }

  return oauth2Provider;
});
