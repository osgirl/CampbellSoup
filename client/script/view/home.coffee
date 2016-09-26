###
	(c) 2016 Julian Gonggrijp
###

'use strict'

define [
	'backbone'
	'templates'
], (bb, JST) ->
	class HomeView extends bb.View
		template: JST['home']
		el: 'body'
		render: -> @$el.html @template {}
