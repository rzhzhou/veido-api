var browserSync = require('browser-sync');

var gulp        = require('gulp');
var concat      = require('gulp-concat');
var filter      = require('gulp-filter');
var less        = require('gulp-less');
var minify      = require('gulp-minify-css');
var rename      = require('gulp-rename');
var sourcemaps  = require('gulp-sourcemaps');
var uglify      = require('gulp-uglify');

var reload      = browserSync.reload;

var dist        = 'build/static/';
var tmpl        = 'build/templates/';


gulp.task('default', ['browser-sync'], function() {
  // gulp.watch(tmpl + '**/*.html', [reload]);
  gulp.watch('src/less/index.css', ['index', reload]);
  gulp.watch('src/less/*.less', ['less', reload]);
  gulp.watch('src/js/login.js', ['js-login', reload]);
  gulp.watch('src/js/app.js', ['js-app', reload]);
  gulp.watch('src/js/dashboard.js', ['js-dashboard', reload]);
  gulp.watch('src/js/table.js', ['js-table', reload]);
  gulp.watch('src/js/settings.js', ['js-settings', reload]);
});

gulp.task('browser-sync', function() {
  browserSync({
    notify: false,
    proxy: '0.0.0.0:8000',
    port: 80,
    open: false
  });
});

gulp.task('index', function() {
  var file = [
    'build/static/vendor/animate/animate.min.css',
    'src/less/index.css'
  ];

  gulp.src(file)
    .pipe(minify())
    .pipe(concat('index.css'))
    .pipe(gulp.dest(dist + 'css'));
});

gulp.task('less', function() {
  gulp.src('src/less/app.less')
    // .pipe(sourcemaps.init())
      .pipe(less())
      .pipe(minify())
    // .pipe(sourcemaps.write(dist + 'css'))
    .pipe(gulp.dest(dist + 'css'));
});


//
// individual JS task
//

gulp.task('js-login', function() {
  gulp.src('src/js/login.js')
      .pipe(uglify())
      .pipe(gulp.dest(dist + 'js'));
});

// gulp.task('js-map', function() {
//   var file = [
//     'vendor/jvectormap/jquery-jvectormap.js',
//     'vendor/jvectormap/jquery-jvectormap-cn-merc-en.js'
//   ];

//   gulp.src(file)
//       .pipe(uglify())
//       .pipe(concat('map.js'))
//       .pipe(gulp.dest(dist + 'js'));
// });

// gulp.task('js-chart', function() {
//   var file = [
//     'vendor/flot/jquery.flot.js',
//     'vendor/flot/jquery.flot.resize.js',
//     'vendor/flot/jquery.flot.categories.js'
//   ];

//   gulp.src(file)
//       .pipe(uglify())
//       .pipe(concat('chart.js'))
//       .pipe(gulp.dest(dist + 'js'));
// });

// gulp.task('js-chart', function() {
//   var file = [
//     'vendor/raphael/raphael-min.js',
//     'vendor/morrisjs/morris.min.js'
//   ];

//   gulp.src(file)
//       // .pipe(uglify())
//       .pipe(concat('chart.js'))
//       .pipe(gulp.dest(dist + 'js'))
// });


gulp.task('js-app', function() {
  gulp.src('src/js/app.js')
      .pipe(uglify())
      .pipe(gulp.dest(dist + 'js'));
});

gulp.task('js-dashboard', function() {
  gulp.src('src/js/dashboard.js')
      .pipe(uglify())
      .pipe(gulp.dest(dist + 'js'));
});

gulp.task('js-datatable', function() {
  var file = [
    'build/static/vendor/DataTables/js/jquery.dataTables.js',
    'build/static/vendor/DataTables/js/dataTables.bootstrap.js'
  ];

  gulp.src(file)
      .pipe(uglify())
      .pipe(concat('datatable.js'))
      .pipe(gulp.dest(dist + 'js'));
});

// gulp.task('js-daterange', function() {
//   var file = [
//     'vendor/moment/moment.js',
//     'vendor/moment/locale/zh-cn.js',
//     'vendor/bootstrap-daterangepicker/daterangepicker.js'
//   ];

//   gulp.src(file)
//       .pipe(uglify())
//       .pipe(concat('daterange.js'))
//       .pipe(gulp.dest(dist + 'js'));
// });

gulp.task('js-table', function() {
  gulp.src('src/js/table.js')
      .pipe(uglify())
      .pipe(gulp.dest(dist + 'js'));
});

gulp.task('js-settings', function() {
  gulp.src('src/js/settings.js')
      .pipe(uglify())
      .pipe(gulp.dest(dist + 'js'));
});

// gulp.task('uncss-homepage', function() {
//   var link = [
//     'http://192.168.1.120:3000/'
//   ];

//   gulp.src('public/css/index.all.css')
//       .pipe(uncss({ html: link }))
//       .pipe(cssmin())
//       .pipe(rename('index.min.css'))
//       .pipe(gulp.dest('public/css'))
// });


// gulp.task('concat-login-css', function() {
//   var cssfile = [
//     'public/css/app.css',
//   ];

//   gulp.src(cssfile)
//     .pipe(concat('login.all.css'))
//     .pipe(gulp.dest('public/css'))
// });

// gulp.task('uncss-login', function() {
//   var link = [
//     'http://192.168.1.120:3000/login'
//   ];

//   gulp.src('public/css/login.all.css')
//       .pipe(uncss({ html: link }))
//       .pipe(cssmin())
//       .pipe(rename('login.min.css'))
//       .pipe(gulp.dest('public/css'))
// });

gulp.task('jquery-form', function() {
  gulp.src('build/static/vendor/jquery-form/jquery.form.js')
      .pipe(uglify())
      .pipe(rename('jquery.form.min.js'))
      .pipe(gulp.dest(dist + 'vendor/jquery-form/'));
});