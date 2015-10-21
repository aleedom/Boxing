angular.module('boxing',['ui.bootstrap'])
    .config(['$interpolateProvider', function($interpolateProvider) {
        $interpolateProvider.startSymbol('{['); //required to work with jinja2
        $interpolateProvider.endSymbol(']}');
    }])
    .controller('boxCtrl', ['$scope', '$http', function($scope, $http){
        $scope.items = [];

        $scope.addItem = function(){
            $scope.items.push({
                'length':$scope.length,
                'width':$scope.width,
                'height':$scope.height,
                'amount':$scope.amount,
            });
            $scope.length = '';
            $scope.width = '';
            $scope.height = '';
            $scope.amount = '';
        };
        $scope.removeItem = function(index){
            $scope.items.splice(index,1);
        };
        $scope.boxOrder = function(){

            $http.post('/api/box_order',$scope.items)
                .success(function(response){
                    $scope.order_volume=response;
                });

        };
        $scope.clearAll = function(){
            $scope.items = [];
        }
    }])
    .controller('modalController', function($scope, $uibModal, $log) {

        $scope.animationsEnabled = true;

        $scope.open = function (size) {
            var modalInstance = $uibModal.open({
                animation: $scope.animationsEnabled,
                templateUrl: '/static/app/modalContent.html',
                controller: 'ModalInstanceController',
                size: size,
                resolve: {
                    items: function () {
                        return $scope.items;
                    }
                }
            });

            modalInstance.result.then(function () {  // close() was called
                $scope.clearAll();
            }, function () {  // close wasn't called
                // do nothing
            });
        };

        $scope.toggleAnimation = function () {
            $scope.animationsEnabled = !$scope.animationsEnabled;
        };
    })
    .controller('ModalInstanceController', function ($scope, $http, $modalInstance, items) {

        $http.post('/api/box_order',items)
            .success(function(response){
                $scope.order_volume=response;
            });


        $scope.new_order = function () {
            $modalInstance.close();
        };

        $scope.cancel = function () {
            $modalInstance.dismiss('cancel');
        };
    });
