###
	(c) 2016 Julian Gonggrijp
###

define [
	'backbone'
	'view/home'
], (bb, HomeView) ->
	'use strict'
	
	homeView = new HomeView
	
	class MainRouter extends bb.Router
		routes:
			'': 'home'
		home: -> homeView.render()
