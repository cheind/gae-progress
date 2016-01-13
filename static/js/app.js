
'use strict';

var progressApp = angular.module('ProgressApp', ['ngRoute', 'ui.bootstrap'])

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

progressApp.filter('timeago', function() {
  return function(dateString) {
    var seconds = Math.floor((new Date(new Date().toUTCString()) - new Date(dateString)) / 1000);
    var interval = Math.floor(seconds / 31536000);

    if (interval > 1) {
      return interval + " years";
    }
    interval = Math.floor(seconds / 2592000);
    if (interval > 1) {
      return interval + " months";
    }
    interval = Math.floor(seconds / 86400);
    if (interval > 1) {
      return interval + " days";
    }
    interval = Math.floor(seconds / 3600);
    if (interval > 1) {
      return interval + " hours";
    }
    interval = Math.floor(seconds / 60);
    if (interval > 1) {
      return interval + " minutes";
    }

    if (seconds < 10) {
      return "moments";
    } else {
      return Math.floor(seconds) + " seconds";
    }
  }
});

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
        // Do something now that user is disconnected
        // The response is always undefined.
      },
      error: function(e) {
        // Handle the error
        // console.log(e);
        // You could point users to manually disconnect if unsuccessful
        // https://plus.google.com/apps
      }
    });
  }

  return oauth2Provider;
});
