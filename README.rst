PyCon SK 2020 Website
#####################

Official `PyCon SK 2020 <https://2020.pycon.sk/>`_ website. And a `staging site <https://staging-2020.pycon.sk/>`_ deployed to GitHub pages.

.. image:: https://travis-ci.org/pyconsk/2020.pycon.sk.svg?branch=master
    :target: https://travis-ci.org/pyconsk/2020.pycon.sk

Contributing
------------

Contributions are welcome. If you found a bug please open an issue at our GitHub repo, or submit a pull request. We do welcome any kind of pull request event if it is just a typo ;)


Project structure
-----------------

**1 branch**:

- ``master`` - the `Flask <http://flask.pocoo.org/>`_ app, templates, static files, translations (make your changes here)


Installation
------------

- clone repository locally::

    git clone https://github.com/pyconsk/2020.pycon.sk.git
    cd 2020.pycon.sk

- install pipenv (`official pipenv documentation instructions <https://pipenv.readthedocs.io/en/latest/install/#installing-pipenv>`_)::

    pip install pipenv

- installs all requirements::

    pipenv install

- setup enviroment variables (required by Flask, windows users can `official flask documentation instructions <http://flask.pocoo.org/docs/1.0/quickstart/#a-minimal-application>`_)::
   
    export FLASK_ENV=development
    export FLASK_APP=pycon.py

- activate pipenv virtual environment::

    pipenv shell

- start flask server, and you can view it in browser (http://127.0.0.1:5000/en/index.html)::

    flask run


Translations
------------

Translations are made with `Flask-Babel <https://pythonhosted.org/Flask-Babel/>`_. All translations are located in ``translations`` directory, update ``messages.po`` with your translations messages.

- collect translation strings from Flask app::

    pybabel extract -F babel.cfg -o messages.pot .

- update translation ``messages.po`` files with collected translation strings::

    pybabel update -i messages.pot -d translations

- compile translated messages and generate ``messages.po`` files::

    pybabel compile -d translations


Generate static site
--------------------

`Frozen-Flask <https://pythonhosted.org/Frozen-Flask/>`_ freezes a Flask application into a set of static files. The result can be hosted without any server-side software other than a traditional web server.

- generate static files, and you can find them in ``docs`` directory::

    python freezer.py

- verify the generated result in browser (http://127.0.0.1:8000/en/index.html)::

    cd docs
    python -m http.server 8000


Continuous Deployment
---------------------

Anything committed to master branch will be automatically deployed on live server. Live site contain only generated static site in ``docs`` directory.


Links
-----

- web: https://2020.pycon.sk
- facebook: https://facebook.com/pyconsk
- twitter: https://twitter.com/pyconsk


License
-------

* MIT license for code (code - GitHub repo)
* CC-BY for content, except sponsors logo's and speakers avatars (consult with particular party if you would like to use their logo or avatar)
* SIL for embedded fonts

For more details read the LICENSE file.
