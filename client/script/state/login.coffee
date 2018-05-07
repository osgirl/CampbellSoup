# (c) 2018 Julian Gonggrijp

define [
	'lodash'
	'core/fsm'
], (_, BackboneFsm) ->
	'use strict'

	BackboneFsm.extend
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
