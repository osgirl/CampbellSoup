###
	(c) 2016 Julian Gonggrijp
###

require [
	'jquery'
	'backbone'
	'global/authentication-aspect'
], ($, bb) ->
	'use strict'
	$ ->
		bb.history.start
			pushState: true
			hashChange: false
