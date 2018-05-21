define [
	'jquery'
], ($) ->
	'use strict'

	deferred = $.Deferred()
	$ -> deferred.resolve $ 'main'
	deferred.promise()
