###
	(c) 2016, 2018 Julian Gonggrijp
###

define [
	'jquery'
	'view/home'
], ($, HomeView) ->
	'use strict'

	# $ = require 'jquery'
	# HomeView = require 'view/home'

	describe 'HomeView', ->
		beforeEach ->
			setFixtures $ '<main>'
			@home = new HomeView()

		it 'renders a title and some intro text', ->
			main = $ 'main'
			@home.$el.appendTo main
			expect(main).toContainElement 'h1'
			expect(main).toContainElement 'p'
			expect(main.find 'h1').toContainText 'CampbellSoup'
			expect(main.find 'p').toContainText 'Welcome'
