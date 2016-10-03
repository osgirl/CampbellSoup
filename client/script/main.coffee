###
	(c) 2016 Julian Gonggrijp
###

require.config
	paths:
		jquery: '../bower_components/jquery/dist/jquery'
		backbone: '../bower_components/backbone/backbone'
		underscore: '../bower_components/lodash/dist/lodash'
		handlebars: '../bower_components/handlebars/handlebars.amd'

require [
	'backbone'
	'router/main'
], (bb, MainRouter) ->
	'use strict'
	new MainRouter()
	bb.history.start
		pushState: true
		hashChange: false
