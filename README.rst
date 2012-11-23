Linode API
==========

Provides dynamic, always up to date, Python bindings for the
`Linode API <http://www.linode.com/api/>`__.

About
-----

The API is dynamically generated from the `API spec <https://api.linode.com/?api_action=api.spec>`__,
provided by Linode.

Dynamically Generated?
^^^^^^^^^^^^^^^^^^^^^^

When :class:`linode.api.API` is imported, its metaclass,
:class:`linode.api.APIGenerator`, will download the Linode API spec and
populate :class:`linode.api.API` with the available methods and their
corresponding docstrings.

.. warning::

   If :class:`linode.api.APIGenerator` can't successfuly download the API
   spec, from Linode, a ``RuntimeError`` exception will be raised and
   :class:`linode.api.API` will have no methods.

Usage
-----

You must provide the API with your Linode API Key (which can be found in
the My Profile section of your dashboard)::

    .. code-block:: python

       from linode.api import API

       linode = API('mykey')

       >>> print linode.key
       jvj8j7I90GnUx219h4nWhG0UEnvNlxCIhj87TbNjza1qd2fJdjMHyN289N1nPGex

Alternatively, you can call :meth:`linode.api.API.user_getapikey`, with
your Linode.com username and password, to fetch your API key automatically::

    .. code-block:: python

       from linode.api import API

       linode = API()
       linode.user_getapikey('myusername', 'mypassword')

       >>> print linode.key
       jvj8j7I90GnUx219h4nWhG0UEnvNlxCIhj87TbNjza1qd2fJdjMHyN289N1nPGex

Once the API is initialized, with a valid API key, you can start managing
your Linodes::

    .. code-block:: python

       from linode.api import API

       linode = API('mykey')

       >>> print linode.linode_list()

.. note::

   See ``help(API)`` for the available functions.

TODO
----

- Add support for batching requests
