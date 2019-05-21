=============================
Django Fio bank payments
=============================

.. image:: https://badge.fury.io/py/dj-fiobank-payments.svg
    :target: https://badge.fury.io/py/dj-fiobank-payments

.. image:: https://travis-ci.org/PetrDlouhy/dj-fiobank-payments.svg?branch=master
    :target: https://travis-ci.org/PetrDlouhy/dj-fiobank-payments

.. image:: https://codecov.io/gh/PetrDlouhy/dj-fiobank-payments/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/PetrDlouhy/dj-fiobank-payments

Retrieve payments from Fio bank API (through fiobank package) and parse them into Payment objects.

Documentation
-------------

The full documentation is at https://dj-fiobank-payments.readthedocs.io.

Quickstart
----------

Install Django Fio bank payments::

    pip install dj-fiobank-payments

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'dj_fiobank_payments.apps.DjFiobankPaymentsConfig',
        ...
    )

Point it to your `Orders` model (should be derived from `dj_fiobank_payments.models.AbstractOrder`:

.. code-block:: python

	 FIOBANK_PAYMENTS_ORDER_MODEL = 'tests.Order'

Features
--------

Creates Payments from Fio statements and pair them with your custom Order model.

Running Tests
-------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install tox
    (myenv) $ tox

Credits
-------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
