CampbellSoup
============
CampbellSoup, the web-based archive of Campbell test questions.

Configuration
-------------
There are default settings in `campbellsoup.defaults`. You can use those for local debugging purposes, although overriding them is recommended. For production use, you should certainly override them.

You can override the defaults with your own settings by copying `campbellsoup/defaults.py` to a file named `config.py` in the project root and changing the values in the file. For production use, it is recommended that you put the configuration file elsewhere on the filesystem, under restrictive access rights. For development use, you may also opt to create a blank `config.py` starting with `from campbellsoup.defaults import *` and just override a few of the parameters. Note that due to limitations in Flask, you need to manually restart the development server after changes to the configuration.

For documentation, see the [Flask documentation][1]. Some clarifications can also be found in `campbellsoup.__doc__`. You pass either the imported module or the module path (as a string) to `campbellsoup.create_application` in order to use your custom settings. Note that module paths are relative to the `campbellsoup` package.

Dependencies
------------
For the Python dependencies, create a Python 3 virtualenv and activate it. `pip install pip-tools` and then run `pip-sync`. For the JavaScript dependencies, install NPM and Grunt, then run `npm install`. For local development, also install Bower and run `bower install`.

Database
--------
The default configuration in `campbellsoup.defaults` assumes a SQLite database. SQLite and PostgreSQL are the only database backends supported by the `requirements.txt`. If you choose a different backend, you will need to install additional libraries. For most backends, including PostgreSQL, you will also need to create a dedicated database and a dedicated user with all privileges on that database. See the [SQLAlchemy documentation][2] for instructions on setting `SQLALCHEMY_DATABASE_URI`.

In order to bootstrap your local database before first running the application, run `python manage.py -c path/to/your/config.py db upgrade`. Run this command again after defining new migrations. In order to define a new migration (after modifying the database schema in campbellsoup.models), run `python manage.py -c path/to/your/config.py db migrate` and edit the generated file. See the [Flask-Migrate documentation][14] for details.

**Note** if you checked out the repository and migrated your database between commits 397a92c and e72a25e (which is unlikely), you need downgrade your database to version 410d73a04b1d before performing migrations associated with later commits.

Local development
-----------------
Make sure that your virtual environment is activated, then run `grunt`. This will do many things:

  - Compile the CoffeeScript, Sass and Mustache sources to browser-ready static assets (these are hidden in `/.tmp` under the project root).
  - Run all unit tests once.
  - Run the Flask-based backend server on port 5000 (this relies on you having created a `config.py` in the project root directory).
  - Watch all sources for changes, automatically recompiling static assets, re-running unit tests and reloading any open browser tabs where applicable.
  - Recompile and rerun the functional tests when changed. Note that the functional tests are not automatically rerun when you change source files. Functional tests are further discussed below.

All subprocesses log to the same single terminal that you run `grunt` from, so the output will be a mess at first. After that, however, you will be grateful for the combined output, as any server hiccups, test failures and compilation errors will automatically come to your attention from a single window. This process keeps running until you kill it with `ctrl-c`.

At your option, you may also run any of the tasks above separately. The required commands are listed below with pointers to further documentation. Refer to the `Gruntfile.coffee` for the definitions and configuration of the Grunt-based tasks.

  - `grunt handlebars` to precompile all Mustache templates except for the `index.mustache` to a single `templates.js` ([grunt-contrib-handlebars][13]).
  - `grunt coffee` to compile all CoffeeScript sources to JavaScript ([grunt-contrib-coffee][3]). `grunt coffee:compile` to limit compilation to the client side scripts or `grunt coffee:functional` to limit compilation to the functional tests.
  - `grunt newer:coffee`, `grunt newer:coffee:compile` or `grunt newer:coffee:functional` to do the same but only with changed sources ([grunt-newer][15]).
  - `grunt clean:develop compile-handlebars:develop` to generate the `index.html` ([grunt-compile-handlebars][4]). The `clean` step is necessary because `compile-handlebars` appends to output files instead of replacing them.
  - `grunt sass postcss` to compile the stylesheets from Sass to CSS ([grunt-sass][18], [grunt-postcss][19]).
  - `grunt symlink` to ensure that the `/bower_components` are accessible from within the `/.tmp` ([grunt-contrib-symlink][6]).
  - `grunt compile` to do all of the above.
  - `grunt server` or `python manage.py [-c ../config.py] runserver -rd` to just run the development server ([flask-script][12]). Keeps running.
  - `grunt watch` to automatically recompile, retest and reload when files change ([grunt-contrib-watch][10]). This includes the functional tests as described above. Note that if you start the static server before the watch task, livereload will not work until you manually refresh the development browser tab. Keeps running.
  - `grunt casperjs` to run all functional tests. This assumes that you already compiled the CoffeeScript sources. ([grunt-casperjs][16], [CasperJS][17])
  - `grunt newer:casperjs` to run only the functional tests that you edited and recompiled.

In order to remove generated files but not the `node_modules` or the `bower_components`, run `grunt clean:all` ([grunt-contrib-clean][11]).

If you want to verify the optimized assets (see below) during development, you can reconfigure your `config.py` to serve the static files from `/dist` instead of `/.tmp`. Override `STATIC_FOLDER` in order to do so.

Deployment
----------
An optimized version of the static assets can be obtained by running `grunt dist`. The optimized files are put in the `/dist` project subdirectory. In this case you do not need the `bower_components`; the external libraries are fetched from CDNs in their minified forms.

You are advised to run the Flask-based backend as a WSGI application from your favourite HTTP server. Create a WSGI file that imports `campbellsoup.create_application` and calls it with the path to your custom settings module.

Serve the static assets under `/static/`.

Directory reference
-------------------

    project root                 (whatever you called it)
    ├── .editorconfig            notation conventions, in-VCS
    ├── .functional-tests        functional tests compiled to JS, out-of-VCS
    ├── .gitignore
    ├── .tmp/                    generated static assets for dev., out-of-VCS
    ├── Gruntfile.coffee         task configuration, in-VCS
    ├── README.md                this file, in-VCS
    ├── bower.json               listing of JS deps, in-VCS
    ├── bower_components/        JS deps during development, out-of-VCS
    ├── campbellsoup             the Flask application package, in-VCS
    │   ├── *.py
    │   └── *_test.py            unit tests belonging to *.py
    ├── client                   static asset sources, in-VCS
    │   ├── script
    │   │   ├── *.coffee
    │   │   └── *_test.coffee    unit tests belonging to *.coffee
    │   ├── style/
    │   └── template/
    ├── config.py                supposed to be written by you, out-of-VCS
    ├── dist/                    generated static assets for depl., out-of-VCS
    ├── doc/                     additional documentation, in-VCS
    ├── functional-tests         functional test sources in Coffee, in-VCS
    ├── manage.py                backend manager, in-VCS
    ├── migrations               Alembic DB migration definitions, in-VCS
    │   ├── ...                  (ignore these)
    │   └── versions/            the actual migrations
    ├── node_modules/            Node and Grunt dependencies, out-of-VCS
    ├── package.json             listing of Node/Grunt deps, in-VCS
    ├── requirements.in          top-level Python package requirements, in-VCS
    └── requirements.txt         generated pinned requirements, in-VCS


(c) 2014 Julian Gonggrijp & Bert Massop
(c) 2016 Julian Gonggrijp


[1]: http://flask.pocoo.org/docs/0.11/config/
[2]: http://docs.sqlalchemy.org/en/rel_1_0/core/engines.html
[3]: https://www.npmjs.com/package/grunt-contrib-coffee
[4]: https://www.npmjs.com/package/grunt-compile-handlebars
[6]: https://www.npmjs.com/package/grunt-contrib-symlink
[8]: https://www.npmjs.com/package/http-proxy
[9]: https://www.npmjs.com/package/grunt-concurrent
[10]: https://www.npmjs.com/package/grunt-contrib-watch
[11]: https://www.npmjs.com/package/grunt-contrib-clean
[12]: https://flask-script.readthedocs.io/en/latest/
[13]: https://www.npmjs.com/package/grunt-contrib-handlebars
[14]: http://flask-migrate.readthedocs.io/en/latest/
[15]: https://www.npmjs.com/package/grunt-newer
[16]: https://www.npmjs.com/package/grunt-casperjs
[17]: http://docs.casperjs.org/
[18]: https://www.npmjs.com/package/grunt-sass
[19]: https://www.npmjs.com/package/grunt-postcss
