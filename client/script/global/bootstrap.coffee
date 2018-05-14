define [
	'jquery'
	'model/account'
	'view/login'
	'view/home'
	'router/main'
	'state/login'
], ($, Account, LoginView, HomeView, MainRouter, LoginFsm) ->
	'use strict'

	account = new Account
	loginView = new LoginView
	homeView = new HomeView
	mainRouter = new MainRouter
	loginFsm = new LoginFsm
	mainElement = $ 'main'

	account.on 'login:success', -> loginFsm.handle 'loginSuccess'
	# account.on 'login:error', -> TODO
	account.on 'logout', -> loginFsm.handle 'logout'
	loginView.on 'login:submit', account.login, account
	loginView.on 'login:cancel', -> loginFsm.handle 'loginCancel'
	mainRouter.on 'route:home', -> loginFsm.handle 'home'
	mainRouter.on 'route:login', -> loginFsm.handle 'login'
	loginFsm.on 'enter:attemptLogin', ->
		mainRouter.navigate 'login'
		mainElement.append loginView.render().el
	loginFsm.on 'exit:attemptLogin', ->
		loginView.remove()
		# TODO: also clear the login form
	loginFsm.on 'enter:authenticated', ->
		mainRouter.navigate 'home'
		mainElement.append homeView.el
	loginFsm.on 'exit:authenticated', -> homeView.remove()
	loginFsm.on 'enter:unauthenticated', -> mainRouter.navigate ''
	# TODO: call account.logout somewhere

	{account, mainRouter, loginFsm}
