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

echo "finsh update"