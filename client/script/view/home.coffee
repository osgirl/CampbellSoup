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
		el: 'body'
		render: -> @$el.html @template {}
