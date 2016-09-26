###
	(c) 2016 Julian Gonggrijp
###

'use strict'

define [
	'backbone'
	'view/home'
], (bb, HomeView) ->
	homeView = new HomeView
	
	class MainRouter extends bb.Router
		routes:
			'': 'home'
		home: -> homeView.render()
