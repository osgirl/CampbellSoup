###
	(c) 2016 Julian Gonggrijp
###

'use strict'

module.exports = (grunt) ->
	
	if grunt.option 'production'
		require('load-grunt-tasks') grunt, scope: 'dependencies'
	else
		jasmineTemplate = require 'grunt-template-jasmine-requirejs'
		require('load-grunt-tasks') grunt
	stripRegExp = (path, ext) -> new RegExp "^#{path}/|\\.#{ext}$", 'g'
	fs = require 'fs'
	
	grunt.initConfig
		pypackage: 'campbellsoup'
		source: 'client'
		script: 'script'
		style: 'style'
		template: 'template'
		templateSrc: '<%= source %>/<%= template %>'
		functional: 'functional-tests'
		stage: '.tmp'
		dist: 'dist'
		
		clean:
			develop: ['<%= stage %>/index.html']
			dist: ['<%= dist %>/index.html']
			all: [
				'<%= stage %>'
				'<%= dist %>'
				'.<%= functional %>'
				'.*cache'
				'**/__pycache__'
				'**/*.{pyc,pyo}'
			]
		
		handlebars:
			options:
				amd: true
				processName: (path) ->
					src = grunt.config('templateSrc')
					pattern = stripRegExp src, 'mustache'
					path.replace pattern, ''
				compilerOptions:
					knownHelpers: {}
					knownHelpersOnly: true
					compat: true
			compile:
				src: [
					'<%= source %>/<%= template %>/**/*.mustache'
					'!<%= source %>/<%= template %>/index.mustache'
				]
				dest: '<%= stage %>/<%= script %>/templates.js'
		
		coffee:
			options:
				bare: true
			compile:
				expand: true
				cwd: '<%= source %>/<%= script %>'
				src: ['**/*.coffee']
				dest: '<%= stage %>/<%= script %>/'
				ext: '.js'
			functional:
				expand: true
				cwd: '<%= functional %>'
				src: ['**/*.coffee']
				dest: '.<%= functional %>/'
				ext: '.js'
		
		'compile-handlebars':
			develop:
				src: '<%= source %>/<%= template %>/index.mustache'
				dest: '<%= stage %>/index.html'
				partials: '<%= stage %>/<%= script %>/*.js'
				templateData:
					production: false
			dist:
				src: '<%= source %>/<%= template %>/index.mustache'
				dest: '<%= dist %>/index.html'
				partials: '<%= stage %>/<%= script %>/*.js'
				templateData:
					production: true
		
		sass:
			compile:
				options:
					includePaths: [
						'node_modules'
					]
					sourceComments: true
				expand: true
				cwd: '<%= source %>/<%= style %>'
				src: ['*.sass', '*.scss']
				dest: '<%= stage %>/<%= style %>'
				ext: '.css.pre'
		
		postcss:
			compile:
				options:
					processors: [
						(require 'autoprefixer') {
							browsers: [
								'Android 2.3'
								'Android >= 4'
								'Chrome >= 20'
								'Firefox >= 24'
								'Explorer >= 8'
								'iOS >= 6'
								'Opera >= 12'
								'Safari >= 6'
							]
						}
					]
				expand: true
				cwd: '<%= stage %>/<%= style %>'
				src: ['*.css.pre']
				dest: '<%= stage %>/<%= style %>'
				ext: '.css'
		
		symlink:
			compile:
				expand: true
				src: [
					'bower_components'
				]
				dest: '<%= stage %>'
		
		shell:
			backend:
				command: (filename) ->
					filename ?= 'config.py'
					"$VIRTUAL_ENV/bin/python manage.py -c ../#{filename} runserver -rd"
			pytest:
				files: [{
					src: ['campbellsoup/**/*_test.py']
				}]
				command: ->
					files = (o.src for o in grunt.config 'shell.pytest.files')
					src = [].concat.apply([], files)
					paths = (grunt.file.expand src).join ' '
					"py.test #{paths}"
		
		jasmine:
			test:
				options:
					specs: '<%= stage %>/<%= script %>/**/*_test.js'
					helpers: [
						'bower_components/jquery/dist/jquery.js'
						'bower_components/jasmine-jquery/lib/jasmine-jquery.js'
					]
					# host: 'http://localhost:8000/'
					template: jasmineTemplate
					templateOptions:
						requireConfigFile: '<%= stage %>/<%= script %>/developConfig.js'
						requireConfig:
							baseUrl: '<%= script %>'
					outfile: '<%= stage %>/_SpecRunner.html'
					display: 'short'
					summary: true
		
		casperjs:
			options:
				silent: true
			functional:
				src: ['.<%= functional %>/**/*.js']
		
		watch:
			handlebars:
				files: '<%= handlebars.compile.src %>'
				tasks: 'handlebars:compile'
			scripts:
				files: '<%= coffee.compile.src %>'
				options:
					cwd:
						files: '<%= coffee.compile.cwd %>'
				tasks: ['newer:coffee:compile', 'jasmine:test']
			sass:
				files: '<%= sass.compile.src %>'
				options:
					cwd:
						files: '<%= sass.compile.cwd %>'
				tasks: ['sass:compile', 'postcss:compile']
			html:
				files: [
					'<%= grunt.config("compile-handlebars.develop.src") %>'
					'<%= stage %>/<%= script %>/developConfig.js'
				]
				tasks: ['clean:develop', 'compile-handlebars:develop']
			python:
				files: '<%= pypackage %>/**/*.py'
				tasks: 'newer:shell:pytest'
			functional:
				files: '<%= coffee.functional.src %>'
				options:
					cwd:
						files: '<%= coffee.functional.cwd %>'
				tasks: ['newer:coffee:functional', 'newer:casperjs:functional']
			config:
				files: 'Gruntfile.coffee'
			livereload:
				files: [
					'<%= script %>/**/*.js'
					'<%= style %>/*.css'
					'*.html'
					'!_SpecRunner.html'
				]
				options:
					cwd:
						files: '<%= stage %>'
					livereload: true
		
		requirejs:
			dist:
				options:
					baseUrl: '<%= stage %>/<%= script %>'
					mainConfigFile: '<%= stage %>/<%= script %>/developConfig.js'
					wrapShim: true
					paths:
						jquery: 'empty:'
						backbone: 'empty:'
						underscore: 'empty:'
						'handlebars.runtime': 'empty:'
					include: ['main.js']
					out: '<%= dist %>/campbellsoup.js'
		
		cssmin:
			dist:
				src: ['<%= stage %>/<%= style %>/*.css']
				dest: '<%= dist %>/campbellsoup.css'
		
		concurrent:
			preserver:
				tasks: ['shell:pytest', 'compile']
			develop:
				tasks: [
					['concurrent:preserver', 'server']
					['watch']
				]
			options:
				logConcurrentOutput: true
		
		newer:
			options:
				override: (info, include) ->
					if info.task == 'shell' and info.target == 'pytest'
						source = info.path.replace /_test\.py$/, '.py'
						fs.stat source, (error, stats) ->
							if stats.mtime.getTime() > info.time.getTime()
								include yes
							else
								include no
					else
						include no
	
	grunt.registerTask 'compile-base', [
		'handlebars:compile'
		'newer:coffee:compile'
		'sass:compile'
		'postcss:compile'
		'symlink:compile'
	]
	grunt.registerTask 'compile', [
		'compile-base'
		'clean:develop'
		'compile-handlebars:develop'
	]
	grunt.registerTask 'dist', [
		'compile-base'
		'clean:dist'
		'compile-handlebars:dist'
		'requirejs:dist'
		'cssmin:dist'
	]
	grunt.registerTask 'server', ['shell:backend']
	grunt.registerTask 'default', ['concurrent:develop']
