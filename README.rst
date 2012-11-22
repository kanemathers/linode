Linode API
==========

Provides Python bindings for the `Linode API <http://www.linode.com/api/>`__.

Usage
-----

The API is dynamically generated from the provided
`Linode spec <https://api.linode.com/?api_action=api.spec>`__. This means,
on import, a HTTP GET request will be made in order to construct the API
class::

    .. code-block:: python

       from linode.api import API

       api     = API('myapikey')
       linodes = api.linode_list()

       >>> print linodes.json

See ``help(API)`` for the available functions.

TODO
----

- Turn API response errors into exceptions. Don't want the user to have to
  manually read out the errors.
- ``**kwargs`` need to be shown in the docstring.
