# (c) 2018 Julian Gonggrijp

define [
	'backbone'
	'lodash'
	'templates'
], (bb, _, JST) ->
	'use strict'

	class BulmaModalView extends bb.View
		template: JST.modal
		tagName: 'div'
		className: 'modal'

		defaultOptions:
			wrap: no
			allowClose: yes
			openInitially: no

		events:
			'click .modal-background, .modal-close': 'userClose'

		initialize: (options) ->
			_.defaults @, options, defaultOptions
			[@insertContent, @wrap] = switch @wrap
				when 'content' then [@insertInContent, content: true]
				when 'card' then [@insertInCard, card: true]
				else [@insertDirectly, false]
			@fetchContent = switch
				when @content?.el?
					# Backbone.View
					@fetchViewContent
				when @content?.get? or @content?.attributes
					# HTML element, possibly wrapped in a jQuery
					@fetchElementContent
