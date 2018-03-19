###
	(c) 2016, 2017 Julian Gonggrijp
###

require.config
	baseUrl: 'static/script'
	paths:
		jquery: '../bower_components/jquery/dist/jquery'
		backbone: '../bower_components/backbone/backbone'
		lodash: '../bower_components/lodash/dist/lodash'
		'handlebars.runtime': '../bower_components/handlebars/handlebars.runtime.amd'
		machina: '../bower_components/machina/lib/machina'
	map:
		'*':
			underscore: 'lodash'

