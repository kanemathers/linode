import textwrap

import requests

from .exceptions import MissingArgument

__all__ = ['API']

class APIGenerator(type):
    """ Linode API Metaclass.

    Downloads the `API spec <https://api.linode.com/?api_action=api.spec>`__
    and builds the available methods into the newly constructed class.
    """

    def __new__(cls, name, bases, dct):
        new_class = super(APIGenerator, cls).__new__(cls, name, bases, dct)

        # TODO: catch errors here and die gracefully
        spec    = requests.get('https://api.linode.com/?api_action=api.spec')
        spec    = spec.json

        version = spec['DATA']['VERSION']
        methods = spec['DATA']['METHODS']

        for i in methods:
            method_name = i.replace('.', '_')
            doc         = methods[i]['DESCRIPTION']
            parameters  = methods[i]['PARAMETERS']

            fn          = build_api_method(i, parameters)
            fn.__doc__  = '\n'.join(textwrap.wrap(doc))
            fn.__name__ = str(method_name)

            setattr(new_class, method_name, fn)

        new_class.version = version

        return new_class

def build_api_method(action, parameters):
    """ Factory for building API methods.

    Returns a new function to perform the specified API ``action``. The
    ``parameters``, provided by Linode, will be used to determine what
    arguments are required for the API call.

    If a required argument is missing, a :class:`exceptions.MissingArgument`
    exception will be raised.
    """

    required = [i for i in parameters if parameters[i]['REQUIRED']]

    def fn(self, **kwargs):
        for k in required:
            if k not in kwargs:
                raise MissingArgument('{0} is a required argument'.format(k))

        request                       = kwargs
        request['api_key']            = self.key
        request['api_action']         = action
        request['api_responseFormat'] = 'json'

        return requests.get('https://api.linode.com/api/', params=request)

    return fn

class API(object):
    """ Linode API.

    Exposes the Linode API methods, provided from the API spec. The Python
    Requests module is used to query the API and, as such, the
    :class:`requests.Response` object is returned.

    .. code-block:: python

       api     = API('myapikey')
       linodes = api.linode_list()

       >>> print linodes.json
    """

    __metaclass__ = APIGenerator

    def __init__(self, api_key):
        self.key = api_key
