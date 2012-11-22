class MissingArgument(Exception):
    """ Raised when a required keyword argument is missing from a function
    call.
    """

    pass

class APIError(Exception):
    """ Raised when the Linode API returns an error.

    :Parameters:
        - `code`: The ERRORCODE returned from Linode
        - `message`: The ERRORMESSAGE returned form Linode
    """

    def __init__(self, code, message):
        self.code    = code
        self.message = message

    def __str__(self):
        return '{0} ({1})'.format(self.message, self.code)

class APIKeyError(Exception):
    """ Raised when a request is attempted with no API key set. """
