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
		
		shell:
			backend:
				command: (filename) ->
					filename ?= 'config.py'
					"$VIRTUAL_ENV/bin/python manage.py -c ../#{filename} runserver -rd"
		
		concurrent:
			server:
				tasks: ['shell:backend', 'connect:server:keepalive']
				options:
					logConcurrentOutput: true
			develop:
				tasks: [['compile', 'jasmine:test', 'watch'], 'server']
				options:
					logConcurrentOutput: true
		
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
		
		watch:
			handlebars:
				files: '<%= handlebars.compile.src %>'
				tasks: 'handlebars:compile'
			scripts:
				files: '<%= coffee.compile.src %>'
				options:
					cwd:
						files: '<%= coffee.compile.cwd %>'
				tasks: ['coffee:compile', 'jasmine:test']
			compass:
				files: '<%= compass.options.sassDir %>/*'
				tasks: 'compass:compile'
			copy:
				files: '<%= copy.compile.src %>'
				options:
					cwd:
						files: '<%= copy.compile.cwd %>'
				tasks: 'copy:compile'
			config:
				files: 'Gruntfile.coffee'
		
		requirejs:
			dist:
				options:
					baseUrl: '<%= stage %>/<%= script %>'
					mainConfigFile: '<%= stage %>/<%= script %>/main.js'
					include: ['main.js']
					out: '<%= dist %>/campbellsoup.js'
	
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
	
	grunt.registerTask 'compile', [
		'handlebars:compile'
		'coffee:compile'
		'compass:compile'
		'copy:compile'
		'symlink:compile'
	]
	grunt.registerTask 'server', ['concurrent:server']
	grunt.registerTask 'default', ['concurrent:develop']
	
	# grunt.registerTask 'default', ['develop']
