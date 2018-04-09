# (c) 2018 Julian Gonggrijp

define [
	'backbone'
	'lodash'
	'model/account'
], (bb, _, Account) ->
	'use strict'

	credentials =
		email: 'bla@bla.com'
		password: 'banana-split'

	data =
		login:
			success:
				id: 1
				email_address: credentials.email
				role:
					id: 1
					name: 'hero'
				person:
					id: 1
					short_name: 'bla'
					full_name: 'blabla'
			error:
				error: 'User does not exist or password is invalid.'

	response =
		login:
			success:
				status: 200
				responseText: JSON.stringify data.login.success
			error:
				status: 401
				responseText: JSON.stringify data.login.error
		logout:
			success:
				status: 205
				responseText: ''
			error:
				status: 500
				responseText: ''

	describe 'AccountModel', ->
		beforeEach ->
			@account = new Account()
			jasmine.Ajax.install()

		afterEach ->
			jasmine.Ajax.uninstall()

		describe '.parse', ->
			beforeEach ->
				@data = data.login.success
				@parseResult = @account.parse @data

			it 'assigns the role to a submodel', ->
				expect(@account.role).toEqual jasmine.any bb.Model
				expect(@account.role.attributes).toEqual @data.role

			it 'assigns the person to a submodel', ->
				expect(@account.person).toEqual jasmine.any bb.Model
				expect(@account.person.attributes).toEqual @data.person

			it 'returns the remaining attributes', ->
				remainingAttributes = _.omit @data, ['role', 'person']
				expect(@parseResult).toEqual remainingAttributes

		describe '.login', ->
			beforeEach ->
				@successHandler = jasmine.createSpy 'successHandler'
				@errorHandler = jasmine.createSpy 'errorHandler'
				@successListener = jasmine.createSpy 'successListener'
				@errorListener = jasmine.createSpy 'errorListener'
				@account.on 'login:success', @successListener
				@account.on 'login:error', @errorListener
				spyOn(@account, 'set').and.callThrough()
				spyOn(@account, 'clear').and.callThrough()
				@promise = @account.login credentials
				@followUp = @promise.then(@successHandler, @errorHandler)
				@request = jasmine.Ajax.requests.mostRecent()

			it 'sends a request', ->
				expect(@request.url).toBe '/api/login'
				expect(@request.method).toBe 'POST'
				expect(@request.data()).toEqual credentials

			it 'does nothing until the response arrives', ->
				expect(@account.set).not.toHaveBeenCalled()
				expect(@account.clear).not.toHaveBeenCalled()
				expect(@successHandler).not.toHaveBeenCalled()
				expect(@errorHandler).not.toHaveBeenCalled()
				expect(@successListener).not.toHaveBeenCalled()
				expect(@errorListener).not.toHaveBeenCalled()
				expect(@account.role).toBeUndefined()
				expect(@account.person).toBeUndefined()
				expect(@account.attributes).toEqual {}

			describe 'on success', ->
				beforeEach ->
					@data = data.login.success
					# Manipulating time because Promise.then is always async.
					# https://github.com/jquery/jquery/issues/3325
					# https://jquery.com/upgrade-guide/3.0/#deferred
					jasmine.clock().install()
					@request.respondWith response.login.success

				afterEach ->
					jasmine.clock().uninstall()

				it 'sets the data on the model', ->
					expect(@account.get 'id').toBe @data.id
					expect(@account.get 'email_address').toBe @data.email_address
					expect(@account.role.attributes).toEqual @data.role
					expect(@account.person.attributes).toEqual @data.person

				it 'emits a success event', ->
					expect(@successListener).toHaveBeenCalled()
					expect(@errorListener).not.toHaveBeenCalled()

				it 'resolves the promise', (done) ->
					expect(@promise.state()).toBe 'resolved'
					@followUp.then =>
						expect(@successHandler).toHaveBeenCalledWith(
							@data              # data
							jasmine.anything() # status
							jasmine.anything() # jqXHR
						)
						expect(@errorHandler).not.toHaveBeenCalled()
						done()
					jasmine.clock().tick(1000)

			describe 'on error', ->
				beforeEach ->
					@data = data.login.error
					# Manipulating time for the same reason as with success.
					jasmine.clock().install()
					@request.respondWith response.login.error

				afterEach ->
					jasmine.clock().uninstall()

				it 'does not set data on the model', ->
					expect(@account.clear).not.toHaveBeenCalled()
					expect(@account.attributes).toEqual {}
					expect(@account.role).toBeUndefined()
					expect(@account.person).toBeUndefined()

				it 'emits an error event', ->
					expect(@successListener).not.toHaveBeenCalled()
					expect(@errorListener).toHaveBeenCalled()

				it 'rejects the promise', (done) ->
					expect(@promise.state()).toBe 'rejected'
					@followUp.then =>
						expect(@successHandler).not.toHaveBeenCalled()
						expect(@errorHandler).toHaveBeenCalledWith(
							jasmine.objectContaining # jqXHR
								responseJSON: @data
							jasmine.anything()       # status
							jasmine.anything()       # errorThrown
						)
						done()
					jasmine.clock().tick(1000)

		describe '.logout', ->
			beforeEach ->
				@successHandler = jasmine.createSpy 'successHandler'
				@errorHandler = jasmine.createSpy 'errorHandler'
				@logoutListener = jasmine.createSpy 'logoutListener'
				@account.on 'logout', @logoutListener
				spyOn(@account, 'set').and.callThrough()
				spyOn(@account, 'clear').and.callThrough()
				@promise = @account.logout()
				@followUp = @promise.then(@successHandler, @errorHandler)
				@request = jasmine.Ajax.requests.mostRecent()

			it 'sends a request', ->
				expect(@request.url).toBe '/api/logout'
				expect(@request.method).toBe 'GET'
				expect(@request.data()).toEqual {}

			it 'does nothing until the response arrives', ->
				expect(@account.set).not.toHaveBeenCalled()
				expect(@account.clear).not.toHaveBeenCalled()
				expect(@successHandler).not.toHaveBeenCalled()
				expect(@errorHandler).not.toHaveBeenCalled()
				expect(@logoutListener).not.toHaveBeenCalled()

			describe 'on success', ->
				beforeEach ->
					# See .login on success for the reason for jasmine.clock.
					jasmine.clock().install()
					@request.respondWith response.logout.success

				afterEach ->
					jasmine.clock().uninstall()

				it 'emits a logout event', ->
					expect(@logoutListener).toHaveBeenCalled()

				it 'resolves the promise', (done) ->
					expect(@promise.state()).toBe 'resolved'
					@followUp.then =>
						expect(@successHandler).toHaveBeenCalled()
						expect(@errorHandler).not.toHaveBeenCalled()
						done()
					jasmine.clock().tick(1000)

			describe '... with pre-existing data', ->
				beforeEach ->
					@account.set id: 2, email_address: 'yada@yada.com'
					@account.role = new bb.Model id: 2, name: 'valet'
					@account.person = new bb.Model id: 2, short_name: 'james'
					@request.respondWith response.logout.success

				it 'clears all data', ->
					expect(@account.attributes).toEqual {}
					expect(@account.role).toBeUndefined()
					expect(@account.person).toBeUndefined()

			describe 'on error', ->
				beforeEach ->
					# Manipulating time for the same reason as with success.
					jasmine.clock().install()
					@request.respondWith response.logout.error

				afterEach ->
					jasmine.clock().uninstall()

				it 'emits no event', ->
					expect(@logoutListener).not.toHaveBeenCalled()

				it 'rejects the promise', (done) ->
					expect(@promise.state()).toBe 'rejected'
					@followUp.then =>
						expect(@successHandler).not.toHaveBeenCalled()
						expect(@errorHandler).toHaveBeenCalled()
						done()
					jasmine.clock().tick(1000)

			describe '... with pre-existing data', ->
				beforeEach ->
					@account.set id: 2, email_address: 'yada@yada.com'
					@account.role = new bb.Model id: 2, name: 'valet'
					@account.person = new bb.Model id: 2, short_name: 'james'
					@changeListener = jasmine.createSpy 'changeListener'
					@account.on 'change', @changeListener
					@request.respondWith response.logout.error

				it 'leaves all data in place', ->
					expect(@account.clear).not.toHaveBeenCalled()
					expect(@changeListener).not.toHaveBeenCalled()
					expect(@account.role).toBeDefined()
					expect(@account.person).toBeDefined()
