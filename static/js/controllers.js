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

progressApp.controller('HomeCtrl', function($scope, $location) {
    $scope.progresses = [];
    $scope.nextPageToken = null;
    $scope.thisPageToken = null;

    $scope.listProgresses = function(args) {
      if (typeof(args)==='undefined') args = {};

      var params = {
        'limit': 5,
        'pageToken': args['pageToken'],
        'order' : args['order'] || '-lastUpdated'
      }
      gapi.client.progressApi.progress.list(params).execute(
        function(resp){
          $scope.$apply(function() {
            $scope.progresses = resp.items;
            $scope.thisPageToken = resp.thisPageToken;
            $scope.nextPageToken = resp.nextPageToken;
          });
        });
    }

    $scope.refreshProgresses = function(args) {
      $scope.listProgresses({'pageToken': $scope.thisPageToken});
    }

    $scope.nextProgresses = function(args) {
      $scope.listProgresses({'pageToken': $scope.nextPageToken});
    }

    $scope.firstProgresses = function(args) {
      $scope.listProgresses({});
    }

    $scope.showCreate = function() {
      $location.path('/create');
    }

    $scope.deleteProgress = function(id) {
      console.log(id);
    }

    $scope.$watch('isSignedIn', function(newValue, oldValue) {
      if (newValue) {
        $scope.listProgresses();
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

  $scope.newApiKey = function() {
    gapi.client.progressApi.progress.generateNewApiKey().execute(
      function(resp){
        $scope.$apply(function() {
          $scope.user['email'] = resp.email;
          $scope.user['apikey'] = resp.apikey;
        });
      });
  }

});

progressApp.controller('CreateCtrl', function($scope, $location) {
  $scope.master = {};

  $scope.create = function(progress) {
     $scope.master = angular.copy(progress);
     gapi.client.progressApi.progress.create(progress).execute(
       function(resp){
         $scope.$apply(function() {
           $location.path("/");
         });
       });
  };


});
