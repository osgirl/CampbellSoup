define [
	'backbone'
	'lodash'
	'machina'
], (bb, _, machina) ->
	'use strict'

	BackboneFsm = machina.Fsm.extend
		constructor: ->
			machina.Fsm.apply this, arguments
			this.on 'transition', ({fromState, toState, action}) =>
				this.emit "exit:#{fromState}", this, action
				this.emit "enter:#{toState}", this, action

	_.extend BackboneFsm.prototype, bb.Events
	BackboneFsm.prototype.emit = BackboneFsm.prototype.trigger

	BackboneFsm
