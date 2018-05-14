###
	(c) 2016, 2018 Julian Gonggrijp
###

define [
	'backbone'
	'templates'
], (bb, JST) ->
	'use strict'

	class HomeView extends bb.View
		template: JST['home']
		tagName: 'article'
		initialize: -> this.render()
		render: ->
			@$el.html @template {}
			@
