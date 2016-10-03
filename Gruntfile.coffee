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
	
	grunt.loadNpmTasks 'grunt-contrib-handlebars'
	grunt.loadNpmTasks 'grunt-contrib-coffee'
	grunt.loadNpmTasks 'grunt-contrib-compass'
	grunt.loadNpmTasks 'grunt-contrib-copy'
	grunt.loadNpmTasks 'grunt-contrib-symlink'
	
	# grunt.registerTask 'default', ['develop']
