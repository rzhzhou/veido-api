'use strict';

var browserSync = require('browser-sync').create(),
    del         = require('del'),
    exec        = require('child_process').exec,

    gulp        = require('gulp'),
    sourcemaps  = require('gulp-sourcemaps'),
    less        = require('gulp-less'),
    minify      = require('gulp-minify-css'),
    concat      = require('gulp-concat'),
    uglify      = require('gulp-uglify'),

    map         = require('./map.json');

var dist = {
  css: 'static/build/css/',
  fonts: 'static/build/fonts/',
  js: 'static/build/js/'
};


// clean up vendor
gulp.task('clean-vendor', function () {
  del.sync([
    dist.css + 'vendor.css',
    dist.fonts + '*',
    dist.js + 'vendor.js'
  ]);
});


// clean up app
gulp.task('clean-app-css', function () {
  del.sync([dist.css + 'app.css']);
});

gulp.task('clean-app-js', function () {
  del.sync([dist.js + 'app.js']);
});

gulp.task('clean-app', [
  'clean-app-css',
  'clean-app-js'
]);


// clean up all
gulp.task('clean', [
  'clean-vendor',
  'clean-app'
]);


// vendor
gulp.task('vendor-css', ['clean-vendor'], function () {
  var files = [
    map.bootstrap.css,
    map.fontawesome.css,
    map.daterangepicker.css
  ];

  return gulp.src(files)
    .pipe(concat('vendor.css'))
    .pipe(minify())
    .pipe(gulp.dest(dist.css));
});

gulp.task('vendor-fonts', ['clean-vendor'], function () {
  var files = [
    map.bootstrap.fonts,
    map.fontawesome.fonts
  ];

  return gulp.src(files)
    .pipe(gulp.dest(dist.fonts));
});

gulp.task('vendor-js', ['clean-vendor'], function () {
  var files = [
    map.jquery,
    map.bootstrap.js,
    map.moment[0],
    map.moment[1],
    map.daterangepicker.js,
    map.twbsPagination,
    map.adminlte,
    map.echarts
  ];

  return gulp.src(files)
    .pipe(concat('vendor.js'))
    // .pipe(uglify())
    .pipe(gulp.dest(dist.js));
});

gulp.task('vendor', [
  'vendor-css',
  'vendor-fonts',
  'vendor-js'
]);


// build
gulp.task('build-less', ['clean-app-css'], function () {
  return gulp.src(map.app.less)
    .pipe(less())
    .pipe(minify())
    .pipe(gulp.dest(dist.css));
});

gulp.task('build-js', ['clean-app-js'], function () {
  return gulp.src(map.app.js)
    .pipe(concat('app.js'))
    .pipe(uglify())
    .pipe(gulp.dest(dist.js));
});

gulp.task('build', [
  'build-less',
  'build-js'
]);


// serve
gulp.task('serve-less', ['clean-app-css'], function () {
  return gulp.src(map.app.less)
    .pipe(sourcemaps.init())
      .pipe(less())
    .pipe(sourcemaps.write())
    .pipe(gulp.dest(dist.css));
});

gulp.task('serve-js', ['clean-app-js'], function () {
  return gulp.src(map.app.js)
    .pipe(concat('app.js'))
    .pipe(gulp.dest(dist.js));
});

gulp.task('django', function () {
  exec('python manage.py runserver 0.0.0.0:8000');
});

gulp.task('serve', ['django'], function () {
  browserSync.init({
    notify: false,
    open: false,
    proxy: '0.0.0.0:8000'
  });

  gulp.watch('static/less/*.less', ['serve-less']);
  gulp.watch('static/js/*.js', ['serve-js']);

  gulp.watch([
    'templates/**/*.html',
    'static/css/*.css',
    'static/js/*.js'
  ]).on('change', browserSync.reload);
});


// default task
gulp.task('default', ['serve']);