###
	(c) 2016 Julian Gonggrijp
###

'use strict'

require.config
	shim:
		handlebars:
			exports: 'Handlebars'
	paths:
		jquery: '../bower_components/jquery/dist/jquery'
		backbone: '../bower_components/backbone/backbone'
		underscore: '../bower_components/lodash/dist/lodash'
		handlebars: '../bower_components/handlebars/handlebars.runtime.amd'

require [
	'backbone'
	'router/main'
], (bb, MainRouter) ->
	new MainRouter()
	bb.history.start
		pushState: true
		hashChange: false
