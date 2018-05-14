###
	(c) 2016 Julian Gonggrijp
###

require [
	'jquery'
	'backbone'
	'global/bootstrap'
], ($, bb) ->
	'use strict'
	$ ->
		bb.history.start
			pushState: true
			hashChange: false
