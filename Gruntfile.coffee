###
	(c) 2016 Julian Gonggrijp
###

'use strict'

module.exports = (grunt) ->
	
	stripRegExp = (path, extension) -> new RegExp "^#{path}/|\\.extension$", 'g'
	
	grunt.initConfig
		source: 'client'
		script: 'script'
		template: 'template'
		templateSrc: '<%= source %>/<%= template %>'
		templatePattern: stripRegExp grunt.config('templateSrc'), 'mustache'
		stage: '.tmp'
		
		handlebars:
			options:
				amd: true
				processName: (path) ->
					pattern = grunt.config 'templatePattern'
					path.replace pattern, ''
				compilerOptions:
					knownHelpers: {}
					knownHelpersOnly: true
			templates:
				src: ['<%= source %>/<%= template %>/**.mustache']
				dest: '<%= stage %>/<%= script %>/templates.js'
		
		coffee:
			options:
				bare: true
			scripts:
				expand: true
				cwd: '<%= source %>/<%= script %>'
				src: ['**/*.coffee']
				dest: '<%= stage %>/<%= script %>/'
				ext: '.js'
	
	grunt.loadNpmTasks 'grunt-contrib-handlebars'
	grunt.loadNpmTasks 'grunt-contrib-coffee'
	
	# grunt.registerTask 'default', ['develop']
