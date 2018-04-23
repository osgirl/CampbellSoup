# (c) 2018 Julian Gonggrijp

define [
	'machina'
	'lodash'
], (machina, _) ->
	'use strict'

	machina.Fsm.extend
		namespace: 'login'
		initialState: 'unauthenticated'
		states:
			unauthenticated:
				_onEnter: -> @clearQueue()
				'*': -> @deferAndTransition 'attemptLogin'
			attemptLogin:
				loginSuccess: 'authenticated'
				loginFail: _.noop
				loginCancel: 'unauthenticated'
				'*': -> @deferUntilTransition()
			authenticated:
				logoff: 'unauthenticated'
