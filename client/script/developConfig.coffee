###
	(c) 2016, 2017 Julian Gonggrijp
###

require.config
	baseUrl: 'static/script'
	paths:
		jquery: '../bower_components/jquery/dist/jquery'
		backbone: '../bower_components/backbone/backbone'
		underscore: '../bower_components/lodash/dist/lodash'
		'handlebars.runtime': '../bower_components/handlebars/handlebars.runtime.amd'
		bootstrap: '../bower_components/bootstrap-sass/assets/javascripts/bootstrap'
	shim:
		'bootstrap/transition': ['jquery']
		'bootstrap/modal': ['jquery']      # has own CSS component
		'bootstrap/dropdown': ['jquery']
		'bootstrap/scrollspy': ['jquery']  # needs CSS nav component
		'bootstrap/tab': ['jquery']        # needs CSS nav component
		'bootstrap/tooltip': ['jquery']    # opt-in, has own CSS component
		'bootstrap/popover': [             # opt-in, has own CSS component
			'jquery'
			'bootstrap/tooltip'
		]
		'bootstrap/alert': ['jquery']
		'bootstrap/button': ['jquery']
		'bootstrap/collapse': [
			'jquery'
			'bootstrap/transition'
		]
		'bootstrap/carousel': ['jquery']   # has own CSS component
		'bootstrap/affix': ['jquery']

