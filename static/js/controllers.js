'use strict';

var progressApp = progressApp || {};

progressApp.controller('RootCtrl', function($scope, oauth2Provider) {
  $scope.isSignedIn = false;

  $scope.trySignIn = function() {
    $scope.signIn(true);
  }

  $scope.signIn = function(immediate) {
    oauth2Provider.signIn(immediate, function(authResp) {
      $scope.$apply(function() {
        $scope.isSignedIn = authResp && !authResp.error;
      });
    });
  };

  $scope.signOut = function() {
    oauth2Provider.signOut();
    $scope.isSignedIn = false;
  };

});

progressApp.controller('HomeCtrl', function($scope) {
    $scope.allProgresses = [];

    $scope.listAllProgresses = function() {
      var params = {'order': '-created'}
      gapi.client.progressApi.progress.list(params).execute(
        function(resp){
          $scope.$apply(function() {
            $scope.allProgresses=resp.items;
          });
        });
    }

    $scope.$watch('isSignedIn', function(newValue, oldValue) {
      if (newValue) {
        $scope.listAllProgresses();
      }
    });
});

progressApp.controller('ProfileCtrl', function($scope) {

  $scope.user = {};

  $scope.getProfile = function() {
    gapi.client.progressApi.progress.user().execute(
      function(resp){
        $scope.$apply(function() {
          $scope.user['email'] = resp.email;
          $scope.user['apikey'] = resp.apikey;
        });
      });
  }

  $scope.$watch('isSignedIn', function(newValue, oldValue) {
    if (newValue) {
      $scope.getProfile();
    }
  });
});
