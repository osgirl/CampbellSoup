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
					prefixPieces = grunt.config('templates').split '/'
					pieces = path.split '/'
					pieces.shift() for piece in prefixPieces
					fileNameParts = pieces.pop().split '.'
					fileNameParts.pop()
					newFileName = fileNameParts.join '.'
					pieces.push newFileName
					pieces.join '/'
				compilerOptions:
					knownHelpers: {}
					knownHelpersOnly: true
			templates:
				src: ['<%= templates %>/**.mustache']
				dest: '<%= stage %>/<%= scripts %>/templates.js'
	
	grunt.loadNpmTasks 'grunt-contrib-handlebars'
	
	# grunt.registerTask 'default', ['develop']
