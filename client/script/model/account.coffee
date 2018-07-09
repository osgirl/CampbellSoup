# (c) 2018 Julian Gonggrijp

define [
	'backbone'
	'lodash'
], (bb, _) ->
	'use strict'

	class AccountModel extends bb.Model
		login: (credentials) ->
			xhr = @save null,
				url: '/api/login'
				attrs: credentials
				success: => @trigger 'login:success'
				error: => @trigger 'login:error'
		activate: (token, credentials) ->
			xhr = @sync 'create', @,
				url: "/api/activate/#{token}"
				contentType: 'application/json'
				data: JSON.stringify credentials
				processData: false
				success: => @trigger 'activate:success'
				error: => @trigger 'activate:error'
		logout: ->
			xhr = @sync 'read', @,
				url: '/api/logout'
				dataType: 'text'
				processData: false
				success: =>
					delete @person
					delete @role
					@clear()
					@trigger 'logout'
		parse: (serverData) ->
			@role = new bb.Model serverData.role
			@person = new bb.Model serverData.person
			_.omit(serverData, ['role', 'person'])
