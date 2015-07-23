'use strict';

var browserSync = require('browser-sync').create(),
    del         = require('del'),

    gulp        = require('gulp'),
    sourcemaps  = require('gulp-sourcemaps'),
    less        = require('gulp-less'),
    minify      = require('gulp-minify-css'),
    concat      = require('gulp-concat'),
    uglify      = require('gulp-uglify');


// miscellaneous

var jsFiles = [
  'bower_components/admin-lte/plugins/slimScroll/jquery.slimscroll.js',
  'src/js/adminlte/app.js',
  'bower_components/twbs-pagination/jquery.twbsPagination.js',
  'src/js/app.js'
];

var dataTablesFiles = [
  'bower_components/DataTables/media/js/jquery.dataTables.js',
  'bower_components/datatables-plugins/integration/bootstrap/3/dataTables.bootstrap.js'
];

gulp.task('dataTables', function() {
  return gulp.src(dataTablesFiles)
    .pipe(concat('dataTables.min.js'))
    .pipe(uglify())
    .pipe(gulp.dest('dist/vendor/dataTables'));
});

gulp.task('clean-css', function() {
  del.sync(['dist/static/css/*.css']);
});

gulp.task('clean-js', function() {
  del.sync(['dist/static/js/*.js']);
});


// tasks for build

gulp.task('build-css', ['clean-css'], function() {
  return gulp.src('src/less/app.less')
    .pipe(less())
    .pipe(minify())
    .pipe(gulp.dest('dist/static/css'));
});

gulp.task('build-js', ['clean-js'], function() {
  return gulp.src(jsFiles)
    .pipe(concat('app.js'))
    .pipe(uglify())
    .pipe(gulp.dest('dist/static/js'));
});

gulp.task('build', ['build-css', 'build-js']);


// tasks for serve

gulp.task('serve-less', ['clean-css'], function() {
  return gulp.src('src/less/app.less')
    .pipe(sourcemaps.init())
      .pipe(less())
    .pipe(sourcemaps.write())
    .pipe(gulp.dest('dist/static/css'));
});

gulp.task('serve-js', ['clean-js'], function() {
  return gulp.src(jsFiles)
    .pipe(concat('app.js'))
    .pipe(gulp.dest('dist/static/js'));
});

gulp.task('serve', function() {
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
