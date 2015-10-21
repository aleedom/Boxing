angular.module('Todo',[])
    .config(['$interpolateProvider', function($interpolateProvider) {
        $interpolateProvider.startSymbol('{['); //required to work with jinja2
        $interpolateProvider.endSymbol(']}');
    }])
    .controller('boxCtrl', ['$scope', '$http', function($scope, $http){
        $scope.todos = [];

        $scope.addItem = function(){
            $scope.todos.push({
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
            $scope.todos.splice(index,1);
        };
        $scope.boxOrder = function(){

            $http.post('/api/box_order',$scope.todos)
                .success(function(response){
                    $scope.order_volume=response;
                });

        };
        $scope.clearAll = function(){
            $scope.todos = [];
        }
    }]);
