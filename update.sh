#!/bin/bash

# remove vendor directory
rm -rf dist/vendor

# copy plugins of adminlte to dist/vendor
cp -r bower_components/admin-lte/plugins dist/vendor

# copy bootstrap to dist/vendor
cp -r bower_components/admin-lte/bootstrap dist/vendor/bootstrap

# copy dist of adminlte to dist/vendor
cp -r bower_components/admin-lte/dist dist/vendor/adminlte

# remove adminlte & bootstrap from src/less
rm -rf src/less/bootstrap
rm -rf src/less/adminlte

# copy build/bootstrap-less to src/less/bootstrap
cp -r bower_components/admin-lte/build/bootstrap-less src/less/bootstrap

# copy build/less to src/less/adminlte
cp -r bower_components/admin-lte/build/less src/less/adminlte

# remove echarts from dist/vendor
rm -rf dist/vendor/echarts

# copy dist of echarts to dist/vendor
cp -r bower_components/echarts/build/dist dist/vendor/echarts

# copy theme of echarts to dist/vendor/echarts
cp -r bower_components/echarts/doc/example/theme/ dist/vendor/echarts/theme

# add fontawesome directory
mkdir dist/vendor/fontawesome

# copy css and fonts to dist/vendor/fontawesome
cp -r bower_components/fontawesome/css dist/vendor/fontawesome/css
cp -r bower_components/fontawesome/fonts dist/vendor/fontawesome/fonts

echo "finish update"