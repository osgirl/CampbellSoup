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
		activeClass: 'is-active'

		defaultOptions:
			wrap: no
			allowClose: yes
			openInitially: no

		events:
			'click .modal-background, .modal-close': 'userClose'

		initialize: (options) ->
			_.defaults @, options, @defaultOptions
			[@insertContent, @wrap] = switch @wrap
				when 'content' then [@insertInContent, content: true]
				when 'card' then [@insertInCard, card: true]
				else [@insertDirectly, false]
			@fetchContent = switch
				when @content?.el?
					# Backbone.View
					@fetchViewContent
				when @content?.get? or @content?.outerHTML?
					# HTML element, possibly wrapped in a jQuery
					@fetchElementContent
				when @content?.toUpperCase?
					# String
					@fetchStringContent
				else
					# no content
					@fetchTrivial
			@userCloseInternal = if @allowClose then @close else _.noop
			@render()
			if @openInitially then @open()

		render: ->
			@$el.html @template @
			@insertContent @fetchContent()
			@

		open: ->
			@$el.addClass @activeClass
			@

		close: ->
			@$el.removeClass @activeClass
			@

		toggle: ->
			@$el.toggleClass @activeClass
			@

		userClose: -> @userCloseInternal()

		insertInContent: (contentElement) ->
			@$('.modal-content').append contentElement

		insertInCard: (contentElement) ->
			@$('.modal-card').append contentElement

		insertDirectly: (contentElement) ->
			@$el.append contentElement

		fetchViewContent: -> @content.el

		fetchElementContent: -> @content

		fetchStringContent: -> bb.$ @content

		fetchTrivial: -> bb.$ '<div>'
