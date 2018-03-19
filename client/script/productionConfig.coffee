###
	(c) 2016, 2017 Julian Gonggrijp
###

require.config
	baseUrl: 'static'
	paths:
		jquery: '//code.jquery.com/jquery-3.1.1.min'
		backbone: '//cdnjs.cloudflare.com/ajax/libs/backbone.js/1.3.3/backbone-min'
		lodash: '//cdnjs.cloudflare.com/ajax/libs/lodash.js/4.16.1/lodash.min'
		'handlebars.runtime': '//cdnjs.cloudflare.com/ajax/libs/handlebars.js/4.0.5/handlebars.runtime.amd.min'
		machina: '//cdn.jsdelivr.net/npm/machina@2.0.2/lib/machina.min'
	map:
		'*':
			underscore: 'lodash'

