###
	(c) 2016 Julian Gonggrijp
###

'use strict'

module.exports = (grunt) ->
	
	grunt.initConfig
		prefix: 'client'
		scripts: '<%= prefix %>/script'
		templates: '<%= prefix %>/template'
		stage: '.tmp'
		
		handlebars:
			options:
				amd: true
				processName: (path) ->
					templateSource = grunt.config('templates')
					pattern = new RegExp "^#{templateSource}/|\\.mustache$", 'g'
					path.replace pattern, ''
				compilerOptions:
					knownHelpers: {}
					knownHelpersOnly: true
			templates:
				src: ['<%= templates %>/**.mustache']
				dest: '<%= stage %>/<%= scripts %>/templates.js'
	
	grunt.loadNpmTasks 'grunt-contrib-handlebars'
	
	# grunt.registerTask 'default', ['develop']
