function init() {
  console.log('init');
  angular.element(document).ready(function() {
    window.init();
  });
}

// declare a Angular JS module
var progressModule = angular.module('progressApp', []);

progressModule.filter('backendStatus', function() {
    return function(input) {
        return input ? 'ready' : 'not ready';
    }
});

progressModule.controller('progressCtrl', function($scope) {
  window.init = function() {
    $scope.$apply($scope.loadProgressApi);
  };
  console.log("in here");
  $scope.progressApiReady = false;
  $scope.allProgresses=[];

  $scope.loadProgressApi = function() {
    var ROOT = '//'+window.location.host +'/_ah/api'
    gapi.client.load('progressApi', 'v1', function(){$scope.progressApiReady =true; $scope.listAllProgresses();}, ROOT);
  }

  $scope.listAllProgresses = function() {
    gapi.client.progressApi.progress.list().execute(
      function(resp){
        $scope.$apply(function() {
          $scope.allProgresses=resp.items;
        });
      });
  }
});
