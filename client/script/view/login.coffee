define [
	'backbone'
	'templates'
], (bb, JST) ->
	'use strict'

	class LoginView extends bb.View

		tagName: 'article'
		className: 'card'
		template: JST.login

		initialize: (options) ->
			@model ?= new bb.Model()

		events:
			'change #login-email': 'updateEmail'
			'change #login-password': 'updatePassword'
			'submit': 'submit'
			'reset': 'cancel'

		render: ->
			@$el.html @template {}
			@$('#login-email').val @model.get 'email'
			@$('#login-password').val @model.get 'password'
			@

		updateEmail: (event) ->
			@model.set 'email', @$(event.target).val()

		updatePassword: (event) ->
			@model.set 'password', @$(event.target).val()

		submit: (event) ->
			event.preventDefault()
			@trigger 'login:submit', @model.toJSON()

		cancel: ->
			@trigger 'login:cancel'
			@model.clear()
