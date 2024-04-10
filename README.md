Create a virtualenv and activate it:

```bash
$ python3 -m venv .venv
$ . .venv/bin/activate
```

Install Flaskr::

    $ pip install -e .

## Run

.. code-block:: text

    $ flask --app flaskr init-db
    $ flask --app flaskr run --debug

Open http://127.0.0.1:5000 in a browser.
