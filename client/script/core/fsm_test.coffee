define [
	'backbone'
	'lodash'
	'core/fsm'
], (bb, _, BackboneFsm) ->
	'use strict'

	TestFsm = BackboneFsm.extend
		initialize: -> @food = 'banana'
		states:
			uninitialized:
				cycle: 'bycicle'
				eat: 'kitchen'
				'*': -> @deferUntilTransition()
			bycicle:
				ring: -> @emit 'bycicleRang'
				eat: -> @deferAndTransition 'kitchen'
				'*': -> @deferUntilTransition()
				_onExit: -> @emit 'stopCycling'
			kitchen:
				_onEnter: -> @clearQueue()
				sleep: 'bed'
			bed:
				cycle: 'bycicle'
				'*': -> @deferAndTransition 'bycicle'

	describe 'BackboneFsm', ->
		beforeEach ->
			@fsm = new TestFsm()
			@messager = _.clone bb.Events

		describe 'has the Backbone.Events interface, which', ->
			beforeEach ->
				@spy1 = jasmine.createSpy 'spy1'
				@spy2 = jasmine.createSpy 'spy2'

			it 'has a trigger method', ->
				expect(@fsm.trigger).toEqual jasmine.any Function

			it 'can be listened on', ->
				@fsm.on 'example1', @spy1
				@fsm.on example2: @spy2
				expect(@spy1).not.toHaveBeenCalled()
				@fsm.trigger 'example1'
				expect(@spy1).toHaveBeenCalled()
				expect(@spy2).not.toHaveBeenCalled()
				@fsm.trigger 'example2'
				expect(@spy2).toHaveBeenCalled()

		describe 'has the machina.Fsm interface, which', ->
			beforeEach ->
				@spies = _.fromPairs _.flatMap ['enter', 'exit'], (direction) ->
					_.map TestFsm.states, (v, state) -> [
						"#{direction}:#{state}"
						jasmine.createSpy "#{direction}_#{state}"
					]
				@fsm.on @spies
