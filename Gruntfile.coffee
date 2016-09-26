###
	(c) 2016 Julian Gonggrijp
###

'use strict'

module.exports = (grunt) ->
	
	stripRegExp = (path, ext) -> new RegExp "^#{path}/|\\.#{ext}$", 'g'
	
	grunt.initConfig
		source: 'client'
		script: 'script'
		style: 'style'
		template: 'template'
		templateSrc: '<%= source %>/<%= template %>'
		stage: '.tmp'
		
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
	
	grunt.loadNpmTasks 'grunt-contrib-handlebars'
	grunt.loadNpmTasks 'grunt-contrib-coffee'
	grunt.loadNpmTasks 'grunt-contrib-compass'
	
	# grunt.registerTask 'default', ['develop']
