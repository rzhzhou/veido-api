'use strict';

var browserSync = require('browser-sync').create(),
    del         = require('del'),
    exec        = require('child_process').exec,

    gulp        = require('gulp'),
    sourcemaps  = require('gulp-sourcemaps'),
    less        = require('gulp-less'),
    minify      = require('gulp-minify-css'),
    concat      = require('gulp-concat'),
    uglify      = require('gulp-uglify');


// paths
var vendor = {
  bootstrap: {
    css: 'node_modules/bootstrap/dist/css/bootstrap.css',
    fonts: 'node_modules/bootstrap/dist/fonts/*',
    js: 'node_modules/bootstrap/dist/js/bootstrap.js'
  },
  daterangepicker: {
    css: 'node_modules/bootstrap-daterangepicker/daterangepicker.css',
    js: 'node_modules/bootstrap-daterangepicker/daterangepicker.js'
  },
  adminlte: 'static/js/adminlte.js',
  echarts: 'static/js/echarts.js',
  fontawesome: {
    css: 'node_modules/fontawesome/css/font-awesome.css',
    fonts: 'node_modules/fontawesome/fonts/*'
  },
  jquery: 'node_modules/jquery/dist/jquery.js',
  moment: [
    'node_modules/moment/moment.js',
    'node_modules/moment/locale/zh-cn.js'
  ],
  twbsPagination: 'node_modules/twbs-pagination/jquery.twbsPagination.js'
};

var app = {
  less: 'static/less/app.less',
  js: [
    'static/js/config.js',
    'static/js/plugin.js',
    'static/js/module.js',
    'static/js/page.js',
    'static/js/route.js'
  ]
};

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
    vendor.bootstrap.css,
    vendor.fontawesome.css,
    vendor.daterangepicker.css
  ];

  return gulp.src(files)
    .pipe(concat('vendor.css'))
    .pipe(minify())
    .pipe(gulp.dest(dist.css));
});

gulp.task('vendor-fonts', ['clean-vendor'], function () {
  var files = [
    vendor.bootstrap.fonts,
    vendor.fontawesome.fonts
  ];

  return gulp.src(files)
    .pipe(gulp.dest(dist.fonts));
});

gulp.task('vendor-js', ['clean-vendor'], function () {
  var files = [
    vendor.jquery,
    vendor.bootstrap.js,
    vendor.moment[0],
    vendor.moment[1],
    vendor.daterangepicker.js,
    vendor.twbsPagination,
    vendor.adminlte,
    vendor.echarts
  ];

  return gulp.src(files)
    .pipe(concat('vendor.js'))
    .pipe(uglify())
    .pipe(gulp.dest(dist.js));
});

gulp.task('vendor', [
  'vendor-css',
  'vendor-fonts',
  'vendor-js'
]);


// build
gulp.task('build-less', ['clean-app-css'], function () {
  return gulp.src(app.less)
    .pipe(less())
    .pipe(minify())
    .pipe(gulp.dest(dist.css));
});

gulp.task('build-js', ['clean-app-js'], function () {
  return gulp.src(app.js)
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
  return gulp.src(app.less)
    .pipe(sourcemaps.init())
      .pipe(less())
    .pipe(sourcemaps.write())
    .pipe(gulp.dest(dist.css));
});

gulp.task('serve-js', ['clean-app-js'], function () {
  return gulp.src(app.js)
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
    'dist/templates/**/*.html',
    'dist/static/css/*.css',
    'dist/static/js/*.js'
  ]).on('change', browserSync.reload);
});


// default task
gulp.task('default', ['serve']);