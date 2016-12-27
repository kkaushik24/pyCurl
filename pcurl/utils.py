import oauth2
import requests
import urllib

from abc import ABCMeta, abstractmethod
from pcurl.constants import GOOGLE_API_KEY, GOOGLE_CX_PARAM
from pcurl.constants import GOOGLE_SEARCH, DUCK_DUCK_GO_SEARCH
from pcurl.constants import  TWITTER_SEARCH, SEARCH_KEY_URL_MAP
from pcurl.constants import TWITTER_CONSUMER_TOKEN, TWITTER_CONSUMER_SECRET
from pcurl.constants import TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_SECRET


class BaseSearchService(object):
    """
    Abstract BaseSearchService class to
    declare minimum methods that every
    search service should implement.
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_rest_url(self):
        """
        This method should return the rest url
        that is called to get the search response
        from the service.

        return:
            rest_url: string
        """
        pass

    @abstractmethod
    def get_search_result(self):
        """
        Here all the logic to get the search result
        should be implemented.

        return:
            error: string
            search_result: string
        """
        pass


class GoogleSearchService(BaseSearchService):
    """
    GoogleSearchService class
    """

    def __init__(self, q):
        self.q = q
        self.service_type = GOOGLE_SEARCH

    def get_rest_url(self):
        """
        Implemented get_rest_url for GoogleSearchService.
        """
        search_url = SEARCH_KEY_URL_MAP.get(self.service_type)
        search_params = {
            'key': GOOGLE_API_KEY,
            'cx': GOOGLE_CX_PARAM,
            'q': self.q
        }
        return '{0}?{1}'.format(search_url,
                                urllib.urlencode(search_params))

    def get_search_result(self):
        """
        Implemented get_search_results for GoogleSearchService.
        """
        error = 'No query provided.'
        search_result = ''
        if self.q:
            rest_url = self.get_rest_url()
            try:
                resp = requests.get(rest_url)
                search_result = resp.content
            except:
                error = 'Error while connecting to {0}'.format(self.service_type)
        return error, search_result


class DuckDuckGoSearchService(BaseSearchService):
    """
    DuckDuckGoSearchService class
    """
    def __init__(self, q):
        self.q = q
        self.service_type = DUCK_DUCK_GO_SEARCH

    def get_rest_url(self):
        """
        Implemented get_rest_url for DuckDuckGoSearchService.
        """

        search_url = SEARCH_KEY_URL_MAP.get(self.service_type)
        search_params = {
            'q': self.q,
            'format': 'json'
        }
        return '{0}?{1}'.format(search_url,
                                urllib.urlencode(search_params))

    def get_search_result(self):
        """
        Implemented get_search_results for DuckDuckGoSearchService.
        """
        error = 'No query provided.'
        search_result = ''
        if self.q:
            rest_url = self.get_rest_url()
            try:
                resp = requests.get(rest_url)
                search_result = resp.content
            except:
                error = 'Error while connecting to {0}'.format(self.service_type)
        return error, search_result


class TwitterSearchService(BaseSearchService):
    """
    TwitterSearchService class
    """

    def __init__(self, q):
        self.q = q
        self.service_type = TWITTER_SEARCH

    def get_rest_url(self):
        """
        Implemented get_rest_url for DuckDuckGoSearchService.
        """

        search_url = SEARCH_KEY_URL_MAP.get(self.service_type)
        search_params = {
            'q': self.q
        }
        return '{0}?{1}'.format(search_url,
                                urllib.urlencode(search_params))

    def get_search_result(self):
        """
        Implemented get_search_results for TwitterSearchService.
        """

        error = 'No query provided.'
        search_result = ''
        if self.q:
            rest_url = self.get_rest_url()
            consumer = oauth2.Consumer(key=TWITTER_CONSUMER_TOKEN,
                                       secret=TWITTER_CONSUMER_SECRET)
            token = oauth2.Token(key=TWITTER_ACCESS_TOKEN,
                                 secret=TWITTER_ACCESS_SECRET)
            client = oauth2.Client(consumer, token)
            try:
                response, content = client.request(rest_url, method="GET",
                                               body="", headers=None)
                search_result = content
            except:
                error = 'Error while connecting to {0}'.format(self.service_type)

        return error, search_result
