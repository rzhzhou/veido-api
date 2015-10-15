'use strict';

var browserSync = require('browser-sync').create(),
    del         = require('del'),
    exec        = require('child_process').exec,
    username    = require('username').sync(),
    lazypipe    = require('lazypipe'),

    gulp        = require('gulp'),
    $           = require('gulp-load-plugins')(),

    env         = require('minimist')(process.argv.slice(2)),
    build       = !!env.production,

    config      = require('./package.json'),
    dist        = config.dist,
    map         = config.map,
    port        = config.port[username];


//
// vendor
//

// clean up
gulp.task('clean-vendor', function () {
  del.sync([
    dist.fonts + '*',
    dist.css + 'vendor.css',
    dist.js + 'vendor.js'
  ]);
});

// fonts
gulp.task('vendor-fonts', ['clean-vendor'], function () {
  var files = [
    map.bootstrap.fonts,
    map.fontawesome.fonts
  ];

  return gulp.src(files)
    .pipe(gulp.dest(dist.fonts));
});

// css
gulp.task('vendor-css', ['clean-vendor'], function () {
  var files = [
    map.bootstrap.css,
    map.fontawesome.css,
    map.daterangepicker.css
  ];

  return gulp.src(files)
    .pipe($.if('!*.min.css', $.minifyCss()))
    .pipe($.concat('vendor.css'))
    .pipe(gulp.dest(dist.css));
});

// js
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
    .pipe($.if('!*.min.js', $.uglify()))
    .pipe($.concat('vendor.js'))
    .pipe(gulp.dest(dist.js));
});

// vendor
gulp.task('vendor', ['vendor-fonts', 'vendor-css', 'vendor-js']);


//
// build --production
//

// clean up css
gulp.task('clean-css', function () {
  del.sync([dist.css + 'app.css']);
});

// less
gulp.task('less', ['clean-css'], function () {
  var development = lazypipe()
      .pipe($.sourcemaps.init)
        .pipe($.less)
      .pipe($.sourcemaps.write);

  var production = lazypipe()
      .pipe($.less)
      .pipe($.minifyCss);

  return gulp.src(map.app.less)
    .pipe($.if(build, production(), development()))
    .pipe(gulp.dest(dist.css));
});

// clean up js
gulp.task('clean-js', function () {
  del.sync([dist.js + 'app.js']);
});

// js
gulp.task('js', ['clean-js'], function () {
  var development = lazypipe()
      .pipe($.jshint, '.jshintrc')
      .pipe($.jshint.reporter, 'jshint-stylish')
      .pipe($.sourcemaps.init)
        .pipe($.concat, 'app.js')
      .pipe($.sourcemaps.write);

  var production = lazypipe()
      .pipe($.uglify)
      .pipe($.concat, 'app.js');

  return gulp.src(map.app.js)
    .pipe($.if(build, production(), development()))
    .pipe(gulp.dest(dist.js));
});

// build
gulp.task('build', ['less', 'js']);


//
// watch changes
//

// django
gulp.task('django', function () {
  exec('python manage.py runserver 0.0.0.0:' + (port * 3));
});

// watch
gulp.task('watch', ['django'], function () {
  browserSync.init({
    notify: false,
    open: false,
    proxy: '0.0.0.0:' + (port * 3),
    port: port
  });

  gulp.watch('static/less/**/*.less', ['less']);
  gulp.watch('static/js/*.js', ['js']);

  gulp.watch([
    'templates/**/*.html',
    'static/css/*.css',
    'static/js/*.js'
  ]).on('change', browserSync.reload);
});


//
// default task
//
gulp.task('default', ['watch']);
