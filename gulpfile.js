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
    css: 'bower_components/bootstrap/dist/css/bootstrap.css',
    fonts: 'bower_components/bootstrap/dist/fonts/*',
    js: 'bower_components/bootstrap/dist/js/bootstrap.js'
  },
  daterangepicker: {
    css: 'bower_components/bootstrap-daterangepicker/daterangepicker.css',
    js: 'bower_components/bootstrap-daterangepicker/daterangepicker.js'
  },
  dataTables: {
    css: 'bower_components/datatables-plugins/integration/bootstrap/3/dataTables.bootstrap.css',
    js: [
      'bower_components/DataTables/media/js/jquery.dataTables.js',
      'bower_components/datatables-plugins/integration/bootstrap/3/dataTables.bootstrap.js'
    ]
  },
  echarts: 'bower_components/echarts/build/dist/echarts-all.js',
  fontawesome: {
    css: 'bower_components/fontawesome/css/font-awesome.css',
    fonts: 'bower_components/fontawesome/fonts/*'
  },
  jquery: 'bower_components/jquery/dist/jquery.js',
  moment: [
    'bower_components/moment/moment.js',
    'bower_components/moment/locale/zh-cn.js'
  ],
  slimscroll: 'bower_components/jquery.slimscroll/jquery.slimscroll.js',
  twbsPagination: 'bower_components/twbs-pagination/jquery.twbsPagination.js'
};

var app = {
  less: 'src/less/app.less',
  js: [
    'src/js/adminlte/app.js',
    'src/js/app.js'
  ]
};

var dist = {
  css: 'dist/static/css/',
  fonts: 'dist/static/fonts/',
  js: 'dist/static/js/'
};


// clean up vendor
gulp.task('clean-vendor-css', function () {
  del.sync([dist.css + 'vendor.css']);
});

gulp.task('clean-vendor-fonts', function () {
  del.sync([dist.fonts + '*']);
});

gulp.task('clean-vendor-js', function () {
  del.sync([dist.js + 'vendor.js']);
});

gulp.task('clean-vendor-echarts', function () {
  del.sync([dist.js + 'echarts-all.js']);
});

gulp.task('clean-vendor', [
  'clean-vendor-css',
  'clean-vendor-fonts',
  'clean-vendor-js',
  'clean-vendor-echarts'
]);


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
gulp.task('vendor-css', ['clean-vendor-css'], function () {
  var files = [
    vendor.bootstrap.css,
    vendor.fontawesome.css,
    vendor.daterangepicker.css,
    vendor.dataTables.css
  ];

  return gulp.src(files)
    .pipe(concat('vendor.css'))
    .pipe(minify())
    .pipe(gulp.dest(dist.css));
});

gulp.task('vendor-fonts', ['clean-vendor-fonts'], function () {
  var files = [
    vendor.bootstrap.fonts,
    vendor.fontawesome.fonts
  ];

  return gulp.src(files)
    .pipe(gulp.dest(dist.fonts));
});

gulp.task('vendor-js', ['clean-vendor-js'], function () {
  var files = [
    vendor.jquery,
    vendor.bootstrap.js,
    vendor.dataTables.js[0],
    vendor.dataTables.js[1],
    vendor.moment[0],
    vendor.moment[1],
    vendor.daterangepicker.js,
    vendor.slimscroll,
    vendor.twbsPagination
  ];

  return gulp.src(files)
    .pipe(concat('vendor.js'))
    .pipe(uglify())
    .pipe(gulp.dest('dist/static/js'));
});

gulp.task('vendor-echarts', ['clean-vendor-echarts'], function () {
  return  gulp.src(vendor.echarts)
    .pipe(gulp.dest(dist.js));
});

gulp.task('vendor', [
  'vendor-css',
  'vendor-fonts',
  'vendor-js',
  'vendor-echarts'
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
  exec('python dist/manage.py runserver');
});

gulp.task('serve', ['django'], function () {
  browserSync.init({
    notify: false,
    open: false,
    proxy: '127.0.0.1:8000'
  });

  gulp.watch('src/less/*.less', ['serve-less']);
  gulp.watch('src/js/*.js', ['serve-js']);

  gulp.watch([
    'dist/templates/**/*.html',
    'dist/static/css/*.css',
    'dist/static/js/*.js'
  ]).on('change', browserSync.reload);
});


// default task
gulp.task('default', ['serve']);
