Templates in CampbellSoup
=========================

You may have noticed that the templates in this directory have file names ending in `.mustache`, while the `bower.json`, the `package.json` and the Gruntfile in the project root directory are all telling you that we are using Handlebars. The reason is that we are *actually* using the Mustache templating language, because of its greater portability, but we compile it on the client side using the Handlebars implementation because it is much faster.

The consequence is that you have to write templates in the subset of Mustache that is compatible with Handlebars (or vice versa). This means that you should NOT use the following features from Mustache:

  - recursive partials;
  - lambdas;
  - alternative delimiters.

You should also NOT use the following features from Handlebars:

  - nested paths;
  - helpers, or anything related to helpers;
  - delimited comments (you can do `{{!-- ... --}}` but such comments cannot
    contain nested mustaches/handlebars).

The lack of both Mustache lambdas and Handlebars helpers means that our templating language is completely logic-free; this is considered a welcome side effect.

I propose to call the intersection of Mustache and Handlebars described here 'MinHandleStache', for lack of a better name.


(c) 2016 Julian Gonggrijp
