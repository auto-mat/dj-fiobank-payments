=====
Usage
=====

To use Django Fio bank payments in a project, add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'dj_fiobank_payments.apps.DjFiobankPaymentsConfig',
        ...
    )

Add Django Fio bank payments's URL patterns:

.. code-block:: python

    from dj_fiobank_payments import urls as dj_fiobank_payments_urls


    urlpatterns = [
        ...
        url(r'^', include(dj_fiobank_payments_urls)),
        ...
    ]
