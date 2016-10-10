###
	(c) 2016 Julian Gonggrijp
###

define [
	'backbone'
	'templates'
], (bb, JST) ->
	'use strict'
	
	class HomeView extends bb.View
		template: JST['home']
		el: 'main'
		render: ->
			@$el.html @template {}
			@
