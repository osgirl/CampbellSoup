###
	(c) 2016 Julian Gonggrijp
###

'use strict'

module.exports = (grunt) ->
	
	stripRegExp = (path, ext) -> new RegExp "^#{path}/|\\.#{ext}$", 'g'
	httpProxy = require 'http-proxy'
	proxy = httpProxy.createProxyServer {}
	
	grunt.initConfig
		source: 'client'
		script: 'script'
		style: 'style'
		template: 'template'
		templateSrc: '<%= source %>/<%= template %>'
		stage: '.tmp'
		dist: 'dist'
		
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
			compile:
				src: ['<%= source %>/<%= template %>/**/*.mustache']
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
		
		compass:
			options:
				sassDir: '<%= source %>/<%= style %>'
			compile:
				options:
					cssDir: '<%= stage %>/<%= style %>'
		
		copy:
			compile:
				expand: true
				cwd: '<%= source %>'
				src: [
					'index.html'
				]
				dest: '<%= stage %>'
		
		symlink:
			compile:
				expand: true
				cwd: '<%= source %>'
				src: [
					'bower_components'
				]
				dest: '<%= stage %>'
		
		connect:
			server:
				options:
					hostname: 'localhost'
					base: '.tmp'
					middleware: (connect, options, middlewares) ->
						middlewares.unshift (req, res, next) ->
							return next() unless req.url.startsWith '/api/'
							req.url = req.url.slice 4
							proxy.web req, res, {
								target: 'http://localhost:5000'
							}
						middlewares
					open: true
					livereload: true
		
		shell:
			backend:
				command: (filename) ->
					filename ?= 'config.py'
					"$VIRTUAL_ENV/bin/python manage.py -c ../#{filename} runserver -rd"
		
		jasmine:
			test:
				options:
					specs: '<%= stage %>/<%= script %>/**/*_test.js'
					helpers: [
						'<%= source %>/bower_components/jquery/dist/jquery.js'
						'<%= source %>/bower_components/jasmine-jquery/lib/jasmine-jquery.js'
					]
					# host: 'http://localhost:8000/'
					template: require 'grunt-template-jasmine-requirejs'
					templateOptions:
						requireConfigFile: '<%= stage %>/<%= script %>/main.js'
						requireConfig:
							baseUrl: '<%= script %>'
					outfile: '<%= stage %>/_SpecRunner.html'
					display: 'short'
					summary: true
		
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
			compass:
				files: '<%= compass.options.sassDir %>/*'
				tasks: 'compass:compile'
			copy:
				files: '<%= copy.compile.src %>'
				options:
					cwd:
						files: '<%= copy.compile.cwd %>'
				tasks: 'newer:copy:compile'
			config:
				files: 'Gruntfile.coffee'
			livereload:
				files: '<%= stage %>/**/*'
				options:
					livereload: true
		
		requirejs:
			dist:
				options:
					baseUrl: '<%= stage %>/<%= script %>'
					mainConfigFile: '<%= stage %>/<%= script %>/productionConfig.js'
					paths:
						jquery: 'empty:'
						backbone: 'empty:'
						underscore: 'empty:'
						handlebars: 'empty:'
					include: ['main.js']
					out: '<%= dist %>/campbellsoup.js'
		
		concurrent:
			server:
				tasks: ['shell:backend', 'connect:server:keepalive']
				options:
					logConcurrentOutput: true
			develop:
				tasks: ['server', ['jasmine:test', 'watch']]
				options:
					logConcurrentOutput: true
	
	grunt.loadNpmTasks 'grunt-contrib-handlebars'
	grunt.loadNpmTasks 'grunt-contrib-coffee'
	grunt.loadNpmTasks 'grunt-contrib-compass'
	grunt.loadNpmTasks 'grunt-contrib-copy'
	grunt.loadNpmTasks 'grunt-contrib-symlink'
	grunt.loadNpmTasks 'grunt-contrib-connect'
	grunt.loadNpmTasks 'grunt-shell'
	grunt.loadNpmTasks 'grunt-concurrent'
	grunt.loadNpmTasks 'grunt-contrib-jasmine'
	grunt.loadNpmTasks 'grunt-contrib-watch'
	grunt.loadNpmTasks 'grunt-contrib-requirejs'
	grunt.loadNpmTasks 'grunt-newer'
	
	grunt.registerTask 'compile', [
		'handlebars:compile'
		'newer:coffee:compile'
		'compass:compile'
		'newer:copy:compile'
		'symlink:compile'
	]
	grunt.registerTask 'server', ['concurrent:server']
	grunt.registerTask 'default', ['compile', 'concurrent:develop']
