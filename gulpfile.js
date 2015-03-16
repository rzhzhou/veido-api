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
  gulp.watch('src/less/*.less', ['less', reload]);
  gulp.watch('src/js/*.js', ['js', reload]);
});

gulp.task('browser-sync', function() {
  browserSync({
    notify: false,
    proxy: '0.0.0.0:8000',
    port: 80,
    open: false
  });
});

gulp.task('less', function() {
  gulp.src('src/less/app.less')
    .pipe(less())
    .pipe(minify())
    .pipe(gulp.dest(dist + 'css'));
});

gulp.task('js', function() {
  var files = [
    'bower_components/admin-lte/plugins/slimScroll/jquery.slimscroll.js',
    'bower_components/DataTables/media/js/jquery.dataTables.js',
    'bower_components/datatables-plugins/integration/bootstrap/3/dataTables.bootstrap.js',
    'src/js/adminlte/app.js',
    'src/js/app.js'
  ];

  gulp.src(files)
    .pipe(concat('app.js'))
    .pipe(uglify())
    .pipe(gulp.dest(dist + 'js'));
});

gulp.task('echarts-theme', function() {
  gulp.src('bower_components/echarts/doc/example/theme/macarons.js')
    .pipe(uglify())
    .pipe(gulp.dest('dist/vendor/echarts/theme'));
});