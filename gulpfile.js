var browserSync = require('browser-sync'),
    reload      = browserSync.reload,

    gulp        = require('gulp'),
    concat      = require('gulp-concat'),
    less        = require('gulp-less'),
    minify      = require('gulp-minify-css'),
    rename      = require('gulp-rename'),
    sourcemaps  = require('gulp-sourcemaps'),
    uglify      = require('gulp-uglify'),

    dist        = 'dist/static/',
    tmpl        = 'dist/templates/';


gulp.task('default', ['browser-sync'], function() {

});

gulp.task('browser-sync', function() {
  browserSync({
    notify: false,
    proxy: '0.0.0.0:8000',
    port: 80,
    open: false
  });
});