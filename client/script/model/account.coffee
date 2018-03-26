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
		logout: ->
			xhr = @sync 'read', @,
				url: '/api/logout'
				processData: false
				success: =>
					delete @person
					delete @role
					@clear()
					@trigger 'logoff'
		parse: (serverData) ->
			@role = new bb.Model serverData.role
			@person = new bb.Model serverData.person
			_.omit(serverData, ['role', 'person'])
