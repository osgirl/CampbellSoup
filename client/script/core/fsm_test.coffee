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
				cycle: 'bicycle'
				eat: 'kitchen'
				'*': -> @deferUntilTransition()
			bicycle:
				ring: -> @emit 'bicycleRang'
				eat: -> @deferAndTransition 'kitchen'
				'*': -> @deferUntilTransition()
				_onExit: -> @emit 'stopCycling'
			kitchen:
				_onEnter: -> @clearQueue()
				sleep: 'bed'
			bed:
				cycle: 'bicycle'
				'*': -> @deferAndTransition 'bicycle'

	describe 'BackboneFsm', ->
		beforeEach ->
			@fsm = new TestFsm()

		describe 'has the Backbone.Events interface, which', ->
			beforeEach ->
				@messager = _.clone bb.Events
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
				@fsm.trigger 'example2', 'foo'
				expect(@spy2).toHaveBeenCalledWith 'foo'

			it 'can be listened on once', ->
				@fsm.once 'test', @spy1
				expect(@spy1.calls.count()).toEqual 0
				@fsm.trigger 'bla'
				expect(@spy1.calls.count()).toEqual 0
				@fsm.trigger 'test'
				expect(@spy1.calls.count()).toEqual 1
				@fsm.trigger 'test'
				expect(@spy1.calls.count()).toEqual 1

			it 'can be listened off', ->
				@fsm.on 'test', @spy1, @
				@fsm.on 'test', @spy1
				@fsm.on 'test', @spy2
				@fsm.trigger 'test'
				@fsm.off null, null, @
				@fsm.trigger 'test'
				@fsm.off null, @spy2
				@fsm.trigger 'test'
				@fsm.off 'test'
				@fsm.trigger 'test'
				expect(@spy1.calls.count()).toEqual 4
				expect(@spy2.calls.count()).toEqual 2

			it 'can listen to another object', ->
				@fsm.listenTo @messager, 'test', @spy1
				@messager.trigger 'test', 'bla'
				expect(@spy1.calls.count()).toEqual 1
				@messager.trigger 'test', 'bla'
				expect(@spy1.calls.count()).toEqual 2
				call = @spy1.calls.mostRecent()
				expect(call.object).toBe @fsm
				expect(call.args).toEqual ['bla']

			it 'can listen to another object once', ->
				@fsm.listenToOnce @messager, 'test', @spy1
				expect(@spy1.calls.count()).toEqual 0
				@messager.trigger 'test', 'bla'
				expect(@spy1.calls.count()).toEqual 1
				@messager.trigger 'test', 'bla'
				expect(@spy1.calls.count()).toEqual 1

			it 'can stop listening to another object', ->
				@fsm.listenTo @messager, 'test', @spy1
				expect(@spy1.calls.count()).toEqual 0
				@messager.trigger 'test', 'bla'
				expect(@spy1.calls.count()).toEqual 1
				@fsm.stopListening @messager, 'test'
				@messager.trigger 'test', 'bla'
				expect(@spy1.calls.count()).toEqual 1

		describe 'has the machina.Fsm interface, which', ->
			beforeEach ->
				@spies =
					transition: jasmine.createSpy 'transition'
					handling: jasmine.createSpy 'handling'
					handled: jasmine.createSpy 'handled'
					nohandler: jasmine.createSpy 'nohandler'
					invalidstate: jasmine.createSpy 'invalidstate'
					deferred: jasmine.createSpy 'deferred'
				@fsm.on @spies

			it 'calls the initialize method', ->
				expect(@fsm.food).toBe 'banana'

			it 'transitions into the initial state', ->
				expect(@fsm.state).toBe 'uninitialized'
				_.forEach @spies, (spy, eventName) ->
					expect(spy).not.toHaveBeenCalled()

			it 'refuses invalid states', ->
				@fsm.transition 'origami'
				expect(@fsm.state).toBe 'uninitialized'
				expect(@spies.transition).not.toHaveBeenCalled()
				expect(@spies.invalidstate).toHaveBeenCalledWith jasmine.objectContaining
					state: 'uninitialized'
					attemptedState: 'origami'

			it 'handles input', ->
				@fsm.handle 'cycle'
				expect(@fsm.state).toBe 'bicycle'
				expect(@fsm.priorState).toBe 'uninitialized'
				expect(@fsm.priorAction).toBe 'uninitialized.cycle'
				_.forEach ['transition', 'handling', 'handled'], (name) =>
					expect(@spies[name].calls.count()).toBe 1
				_.forEach ['nohandler', 'invalidstate', 'deferred'], (name) =>
					expect(@spies[name].calls.count()).toBe 0
				expect(@spies.transition).toHaveBeenCalledWith jasmine.objectContaining
					fromState: 'uninitialized'
					toState: 'bicycle'
				expect(@spies.handling).toHaveBeenCalledWith jasmine.objectContaining
					inputType: 'cycle'
				expect(@spies.handled).toHaveBeenCalledWith jasmine.objectContaining
					inputType: 'cycle'

			it 'queues up actions and clears the queue', ->
				@fsm.handle 'test1'
				@fsm.handle 'test2'
				expect(@fsm.inputQueue.length).toBe 2
				_.forEach ['handling', 'handled', 'deferred'], (name) =>
					expect(@spies[name].calls.count()).toBe 2
				_.forEach ['transition', 'nohandler', 'invalidstate'], (name) =>
					expect(@spies[name].calls.count()).toBe 0
				expect(@spies.deferred).toHaveBeenCalledWith jasmine.objectContaining
					state: 'uninitialized'
					queuedArgs: jasmine.any Object
				@fsm.handle 'cycle'
				expect(@fsm.inputQueue.length).toBe 2
				_.forEach ['handling', 'handled'], (name) =>
					expect(@spies[name].calls.count()).toBe 5
				expect(@spies.deferred.calls.count()).toBe 4
				@fsm.handle 'eat'
				expect(@fsm.inputQueue.length).toBe 0
				_.forEach ['handling', 'handled'], (name) =>
					expect(@spies[name].calls.count()).toBe 6
				expect(@spies.deferred.calls.count()).toBe 5
				expect(@spies.transition.calls.count()).toBe 2
				_.forEach ['nohandler', 'invalidstate'], (name) =>
					expect(@spies[name].calls.count()).toBe 0

			it 'keeps track of the state', ->
				@fsm.handle 'zoo'
				expect(@fsm.state).toBe 'uninitialized'
				@fsm.handle 'eat'
				expect(@fsm.state).toBe 'kitchen'
				expect(@spies.nohandler).not.toHaveBeenCalled()
				@fsm.handle 'eat'
				expect(@spies.nohandler).toHaveBeenCalledWith jasmine.objectContaining
					inputType: 'eat'
					args: jasmine.any Array
				expect(@fsm.state).toBe 'kitchen'
				@fsm.handle 'sleep'
				expect(@fsm.state).toBe 'bed'
				@fsm.handle 'cycle'
				expect(@fsm.state).toBe 'bicycle'
				@fsm.handle 'ring'
				expect(@fsm.state).toBe 'bicycle'
				@fsm.handle 'game'
				expect(@fsm.state).toBe 'bicycle'
				@fsm.handle 'eat'
				expect(@fsm.state).toBe 'kitchen'
				@fsm.handle 'sleep'
				expect(@fsm.state).toBe 'bed'
				@fsm.handle 'eat'
				expect(@fsm.state).toBe 'kitchen'

			it 'emits custom events', ->
				onBicycleRang = jasmine.createSpy 'onBicycleRang'
				onStopCycling = jasmine.createSpy 'onStopCycling'
				@fsm.on 'bicycleRang', onBicycleRang
				@fsm.on 'stopCycling', onStopCycling
				@fsm.transition 'bicycle'
				expect(onBicycleRang).not.toHaveBeenCalled()
				@fsm.handle 'ring'
				expect(onBicycleRang).toHaveBeenCalled()
				expect(onStopCycling).not.toHaveBeenCalled()
				@fsm.handle 'eat'
				expect(onStopCycling).toHaveBeenCalled()


		describe 'has an additional events interface, which', ->
			beforeEach ->
				@spies = _.fromPairs _.flatMap ['enter', 'exit'], (direction) ->
					_.map TestFsm.prototype.states, (v, state) -> [
						"#{direction}:#{state}"
						jasmine.createSpy "#{direction}_#{state}"
					]
				@fsm.on @spies

			it 'fires additional exit:state and enter:state events', ->
				expect(@spies['exit:uninitialized']).not.toHaveBeenCalled()
				expect(@spies['enter:bicycle']).not.toHaveBeenCalled()
				@fsm.handle 'cycle'
				expect(@spies['exit:uninitialized']).toHaveBeenCalledWith @fsm, 'uninitialized.cycle'
				expect(@spies['enter:bicycle']).toHaveBeenCalledWith @fsm, 'uninitialized.cycle'
				expect(@spies['exit:bicycle']).not.toHaveBeenCalled()
				expect(@spies['enter:kitchen']).not.toHaveBeenCalled()
				@fsm.handle 'eat'
				expect(@spies['exit:bicycle']).toHaveBeenCalled()
				expect(@spies['enter:kitchen']).toHaveBeenCalled()
				expect(@spies['exit:kitchen']).not.toHaveBeenCalled()
				expect(@spies['enter:bed']).not.toHaveBeenCalled()
				@fsm.handle 'sleep'
				expect(@spies['exit:kitchen']).toHaveBeenCalled()
				expect(@spies['enter:bed']).toHaveBeenCalled()
				expect(@spies['exit:bed']).not.toHaveBeenCalled()
				expect(@spies['enter:uninitialized']).not.toHaveBeenCalled()
