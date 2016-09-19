CampbellSoup
============
CampbellSoup, the web-based archive of Campbell test questions.

Configuration
-------------
There are default settings in `campbellsoup.defaults`. You can use those for local debugging purposes, although overriding them is recommended. For production use, you should certainly override them.

You can override the defaults with your own settings by copying `campbellsoup/defaults.py` to some other location and changing the values in the file. For documentation, see the [Flask documentation][1]. Some clarifications can also be found in `campbellsoup.__doc__`. You pass either the imported module or the module path (as a string) to `campbellsoup.create_application` in order to use your custom settings. Note that module paths are relative to the `campbellsoup` package.

Testing
-------
Install the `pytest` package using `pip` and run `py.test` from the root directory in order to run all Python unittests. This will use the default settings where applicable.

Local development server
------------------

    python manage.py runserver -?

Use the `-c` option to pass the path to your custom settings module. The server runs at localhost on port 5000.

Production server
-------
You are advised to run CampbellSoup as a WSGI application from your favourite HTTP server. Create a WSGI file that imports `campbellsoup.create_application` and calls it with the path to your custom settings module.


(c) 2014 Julian Gonggrijp & Bert Massop


[1]: http://flask.pocoo.org/docs/0.11/config/
