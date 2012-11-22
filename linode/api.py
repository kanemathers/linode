import textwrap

import requests

from .exceptions import (
    MissingArgument,
    APIError,
    APIKeyError,
    )

__all__ = ['API']

class APIGenerator(type):
    """ Linode API Metaclass.

    Downloads the `API spec <https://api.linode.com/?api_action=api.spec>`__
    and builds the available methods into the newly constructed class.
    """

    def __new__(cls, name, bases, dct):
        new_class = super(APIGenerator, cls).__new__(cls, name, bases, dct)

        try:
            spec = requests.get('https://api.linode.com/?api_action=api.spec')
            spec = spec.json
        except requests.exceptions.RequestException:
            raise RuntimeWarning('Failed to fetch API spec from '
                                 'api.linode.com')

        version = spec['DATA']['VERSION']
        methods = spec['DATA']['METHODS']

        for i in methods:
            (name, fn) = build_api_method(i, methods[i])

            setattr(new_class, name, fn)

        new_class.version = version

        return new_class

def build_api_method(action, info):
    """ Factory for building API methods.

    Given an API ``action`` and the information returned from the API,
    ``info``, returns a new function to perform the action.

    Raises :class:`exceptions.MissingArgument` if a required argument is
    missing.
    """

    name     = action.replace('.', '_')
    doc      = textwrap.wrap(info['DESCRIPTION'])
    params   = info['PARAMETERS']
    required = set()
    raises   = info['THROWS']

    if params:
        doc    += ['', ':Parameters:', '']
        wrapper = textwrap.TextWrapper(initial_indent='    ',
                                       subsequent_indent='       ',
                                       width=66)

        for param in params:
            info = '- `{0}`: {1}'.format(param, params[param]['DESCRIPTION'])

            if not params[param]['REQUIRED']:
                info = '{0} (optional)'.format(info)
            else:
                required.add(param)

            doc += wrapper.wrap(info)

    if raises:
        doc   += ['']
        raises = raises.split(',')

        for exc in raises:
            doc += ['Raises :class:exceptions.APIError ({0})'.format(exc)]

    def fn(self, **kwargs):
        if not self.key and action != 'user.getapikey':
            raise APIKeyError('No API key set. You must call '
                              ':class:`API.user_getapikey`.')

        for k in required:
            if k not in kwargs:
                raise MissingArgument('{0} is a required argument'.format(k))

        request                       = kwargs
        request['api_key']            = self.key
        request['api_action']         = action
        request['api_responseFormat'] = 'json'

        resp = requests.get('https://api.linode.com/', params=request)
        resp = resp.json

        if resp['ERRORARRAY']:
            # we obviously can't raise multiple exceptions. so we'll let
            # user handle them one at a time.
            error = resp['ERRORARRAY'].pop()

            raise APIError(error['ERRORCODE'], error['ERRORMESSAGE'])

        if action == 'user.getapikey':
            self.key = resp['DATA']['API_KEY']

        return resp

    fn.__doc__  = '\n'.join(doc)
    fn.__name__ = str(name)

    return (name, fn)

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

    def __init__(self, api_key=None):
        """ Initialize the API by providing your Linode API key; which can
        be obtained from your Linode Profile page.

        Alternatively, provide no API key and call
        :class:`API.user_getapikey`.
        """

        self.key = api_key
