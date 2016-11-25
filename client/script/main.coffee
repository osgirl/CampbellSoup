###
	(c) 2016 Julian Gonggrijp
###

require [
	'jquery'
	'backbone'
	'router/main'
], ($, bb, MainRouter) ->
	'use strict'
	$ ->
		new MainRouter()
		bb.history.start
			pushState: true
			hashChange: false
