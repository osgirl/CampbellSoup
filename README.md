CampbellSoup
============
CampbellSoup, the web-based archive of Campbell test questions.

Configuration
-------------
There are default settings in `campbellsoup.defaults`. You can use those for local debugging purposes, although overriding them is recommended. For production use, you should certainly override them.

You can override the defaults with your own settings by copying `campbellsoup/defaults.py` to a file named `config.py` in the project root and changing the values in the file. For documentation, see the [Flask documentation][1]. Some clarifications can also be found in `campbellsoup.__doc__`. You pass either the imported module or the module path (as a string) to `campbellsoup.create_application` in order to use your custom settings. Note that module paths are relative to the `campbellsoup` package.

Dependencies
------------
Create a virtualenv and activate it. `pip install pip-tools` and then run `pip-sync`.

Database
--------
The default configuration in `campbellsoup.defaults` assumes a SQLite database. This is also the only database backend supported by the `requirements.txt`. If you choose a different backend, you will need to install additional libraries. For PostgreSQL, which we recommend, use `pip install psycopg2`. For most backends, including PostgreSQL, you will also need to create a dedicated database and a dedicated user with all privileges on that database. See the [SQLAlchemy documentation][2] for instructions on setting `SQLALCHEMY_DATABASE_URI`.

In order to bootstrap your local database before first running the application, run `python manage.py -c path/to/your/config.py db upgrade`. Run this command again after defining new migrations. In order to define a new migration (after modifying the database schema in campbellsoup.models), run `python manage.py -c path/to/your/config.py db migrate` and edit the generated file.

Testing
-------
Install the `pytest` package using `pip` and run `py.test` from the root directory in order to run all Python unittests. This will use the default settings where applicable.

Local development server
------------------

Make sure that your virtual environment is activated. Then, the following command serves the frontend files from `.tmp` while also proxying requests to `/api/*` to the Flask backend server:

    grunt concurrent:server

If you wish to only serve the frontend files, use

    grunt connect:server

When using one of the above commands, the frontend will be available from localhost on port 8000.

If you wish to only run the backend, use

    python manage.py runserver -?

Use the `-c` option to pass the path to your custom settings module (this is `../config.py` if you followed the instructions in the Configuration section). The server runs at localhost on port 5000.

Production server
-------
You are advised to run CampbellSoup as a WSGI application from your favourite HTTP server. Create a WSGI file that imports `campbellsoup.create_application` and calls it with the path to your custom settings module.


(c) 2014 Julian Gonggrijp & Bert Massop
(c) 2016 Julian Gonggrijp


[1]: http://flask.pocoo.org/docs/0.11/config/
