###
	(c) 2016, 2018 Julian Gonggrijp
###

define [
	'backbone'
], (bb) ->
	'use strict'

	class MainRouter extends bb.Router
		routes:
			'(home)': 'home'
			'login': 'login'
