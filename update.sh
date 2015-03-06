#!/bin/bash

# clean up and create folder
rm -rf dist/vendor
mkdir dist/vendor

# copy and rename jquery
cp -r bower_components/admin-lte/plugins/jQuery dist/vendor/jquery
mv dist/vendor/jquery/jQuery-2.1.3.min.js dist/vendor/jquery/jquery.min.js

# copy bootstrap
mkdir dist/vendor/bootstrap
cp -r bower_components/admin-lte/bootstrap/css dist/vendor/bootstrap/css
cp -r bower_components/admin-lte/bootstrap/js dist/vendor/bootstrap/js

# copy echarts
cp -r bower_components/echarts/build/dist dist/vendor/echarts

# copy fontawesome
mkdir dist/vendor/fontawesome
cp -r bower_components/fontawesome/css dist/vendor/fontawesome/css
cp -r bower_components/fontawesome/fonts dist/vendor/fontawesome/fonts

# copy adminlte source code
rm -rf src/less/bootstrap
rm -rf src/less/adminlte
cp -r bower_components/admin-lte/build/bootstrap-less src/less/bootstrap
cp -r bower_components/admin-lte/build/less/ src/less/adminlte
rm -rf src/js/adminlte
cp -r bower_components/admin-lte/dist/js src/js/adminlte


echo "finish update"