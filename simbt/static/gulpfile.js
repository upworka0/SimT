var gulp = require('gulp');
var browserify = require('browserify');
var babelify = require('babelify');
var source = require('vinyl-source-stream');
var gutil = require('gulp-util');
var sass = require('gulp-sass');
var prettify = require('gulp-jsbeautifier');

// Lets bring es6 to es5 with this.
// Babel - converts ES6 code to ES5 - however it doesn't handle imports.
// Browserify - crawls your code for dependencies and packages them up
// into one file. can have plugins.
// Babelify - a babel plugin for browserify, to make browserify
// handle es6 including imports.
gulp.task('es6', function() {
	browserify({
    	entries: './js/main.js',
    	debug: true
  	})
    .transform(babelify.configure({
      presets: ["es2015"]
    }))
    .on('error',gutil.log)
    .bundle()
    .on('error',gutil.log)
    .pipe(source('bundle.js'))
    .pipe(gulp.dest('./js/'));
});

gulp.task('sass', function(){
  return gulp.src('./scss/*.scss')
          .pipe(sass.sync().on('error', sass.logError))
          .pipe(gulp.dest('./css'));
});

gulp.task('prettify-js', function(){
  gulp.src(['./js/**/*.js'])
      .pipe(prettify())
      .pipe(gulp.dest('./js/'));
});

gulp.task('watch',function() {
	gulp.watch('**/*.js',['es6'])
});

gulp.task('sass:watch', function(){
  gulp.watch('./scss/**/*.scss', ['sass']);
})

gulp.task('default', ['watch']);
