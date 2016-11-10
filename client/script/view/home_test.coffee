###
	(c) 2016 Julian Gonggrijp
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
			@home.render()
			main = $ 'main'
			expect(main.children()).toHaveLength 2
			expect(main).toContainElement 'h1'
			expect(main).toContainElement 'p'
			expect(main.children 'h1').toContainText 'CampbellSoup'
			expect(main.children 'p').toContainText 'Welcome'
		
		it 'fails if you want to', ->
			expect(false).toBe true
