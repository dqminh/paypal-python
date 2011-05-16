# coding=utf-8
"""
PayPalResponse parsing and processing.
"""
try:
    from urlparse import parse_qs
except ImportError:
    from cgi import parse_qs

try:
    import simplejson as json
except ImportError:
    import json

import paypal.exceptions

class PayPalResponse(object):
    """
    Parse and prepare the reponse from PayPal's API. Acts as somewhat of a
    glorified dictionary for API responses.

    NOTE: Don't access self.raw directly. Just do something like
    PayPalResponse.someattr, going through PayPalResponse.__getattr__().
    """
    def __init__(self, query_string, config):
        """
        query_string is the response from the API, in NVP format. This is
        parseable by urlparse.parse_qs(), which sticks it into the self.raw
        dict for retrieval by the user.
        """
        # A dict of NVP values. Don't access this directly, use
        # PayPalResponse.attribname instead. See self.__getattr__().
        self.raw = parse_qs(query_string)
        self.config = config

    def __str__(self):
        return str(self.raw)

    def __getattr__(self, key):
        """
        Handles the retrieval of attributes that don't exist on the object
        already. This is used to get API response values.
        """
        # PayPal response names are always uppercase.
        key = key.upper()
        try:
            value = self.raw[key]
            if len(value) == 1:
                return value[0]
            return value
        except KeyError:
            if self.config.KEY_ERROR:
                raise AttributeError(self)
            else:
                return None

    def success(self):
        """
        Checks for the presence of errors in the response. Returns True if
        all is well, False otherwise.
        """
        return self.ack.upper() in (self.config.ACK_SUCCESS,
                                    self.config.ACK_SUCCESS_WITH_WARNING)
    success = property(success)


class AdaptivePayPalResponse(object):
    """
    Parse and prepare the response from PayPal's Adaptive API
    """
    def __init__(self, json_string, config):
        """
        json_string is the response from API in JSON format. It includes a `pay
        key` which is a token you use in subsequent calls to Adaptive Payment
        API to identify this particular payment
        """
        self.config = config;
        self.json = json.loads(json_string)

    def __str__(self):
        return str(self.json)

    def __getattr__(self, key):
        try:
            return self.json[key]
        except KeyError:
            if self.config.KEY_ERROR:
                print "KeyError: " + key
                raise AttributeError(self)
            else:
                return None
