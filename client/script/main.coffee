###
	(c) 2016 Julian Gonggrijp
###

require [
	'backbone'
	'global/domLoadedPromise'
	'global/authentication-aspect'
], (bb, domLoaded) ->
	'use strict'
	domLoaded.then ->
		bb.history.start
			pushState: true
			hashChange: false
