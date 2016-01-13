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

progressApp.controller('HomeCtrl', function($scope, $location, $uibModal) {
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

    $scope.refreshProgresses = function() {
      $scope.listProgresses({'pageToken': $scope.thisPageToken});
    }

    $scope.nextProgresses = function() {
      $scope.listProgresses({'pageToken': $scope.nextPageToken});
    }

    $scope.firstProgresses = function() {
      $scope.listProgresses({});
    }

    $scope.createProgress = function() {
      var modalInstance = $uibModal.open({
        animation: false,
        templateUrl: '/views/create_modal.html',
        controller: 'CreateCtrl',
        size: 'lg',
      });

      modalInstance.result.then(function (progress) {
        gapi.client.progressApi.progress.create(progress).execute(
          function(resp){
            $scope.$apply(function() {
              if (resp && !resp.error) {
                $scope.refreshProgresses();
              }
            });
          });
      });
    }

    $scope.editProgress = function(index) {
      var modalInstance = $uibModal.open({
        animation: false,
        templateUrl: '/views/edit_modal.html',
        controller: 'EditCtrl',
        size: 'lg',
        resolve: {
          progress: function () {
            return $scope.progresses[index];
          }
        }
      });

      modalInstance.result.then(function (progress) {
        gapi.client.progressApi.progress.update(progress).execute(
          function(resp){
            $scope.$apply(function() {
              if (resp && !resp.error) {
                $scope.refreshProgresses();
              }
            });
          });
      });
    }

    $scope.deleteProgress = function(index) {
      var params = {'id': $scope.progresses[index].id}
      gapi.client.progressApi.progress.delete(params).execute(
        function(resp){
          $scope.$apply(function() {
            if (resp && !resp.error) {
              $scope.refreshProgresses();
            }
          });
        });
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

progressApp.controller('CreateCtrl', function($scope, $uibModalInstance) {

  $scope.ok = function () {
    $uibModalInstance.close($scope.progress);
  };

  $scope.cancel = function () {
    $uibModalInstance.dismiss('cancel');
  };
});

progressApp.controller('EditCtrl', function($scope, $uibModalInstance, progress) {
  $scope.progress = angular.copy(progress);

  $scope.ok = function () {
    $uibModalInstance.close($scope.progress);
  };

  $scope.cancel = function () {
    $uibModalInstance.dismiss('cancel');
  };
});
