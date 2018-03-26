# (c) 2018 Julian Gonggrijp

define [
	'machina'
], (machina) ->
	'use strict'

	noop = -> undefined

	machina.Fsm.extend
		namespace: 'login'
		initialState: 'unauthenticated'
		states:
			unauthenticated:
				_onEnter: -> @clearQueue()
				'*': -> @deferAndTransition 'attemptLogin'
			attemptLogin:
				loginSuccess: 'authenticated'
				loginFail: noop
				loginCancel: 'unauthenticated'
				'*': -> @deferUntilTransition()
			authenticated:
				logoff: 'unauthenticated'
