import oauth2
import requests
import urllib
import time

from abc import ABCMeta, abstractmethod
from pcurl.constants import GOOGLE_API_KEY, GOOGLE_CX_PARAM
from pcurl.constants import GOOGLE_SEARCH, DUCK_DUCK_GO_SEARCH
from pcurl.constants import  TWITTER_SEARCH, SEARCH_KEY_URL_MAP
from pcurl.constants import TWITTER_CONSUMER_TOKEN, TWITTER_CONSUMER_SECRET
from pcurl.constants import TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_SECRET


class BaseSearchService(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_rest_url(self):
        pass

    @abstractmethod
    def get_search_result(self):
        pass


class GoogleSearchService(BaseSearchService):
    def __init__(self, q):
        self.q = q
        self.service_type = GOOGLE_SEARCH

    def get_rest_url(self):
        search_url = SEARCH_KEY_URL_MAP.get(self.service_type)
        search_params = {
            'key': GOOGLE_API_KEY,
            'cx': GOOGLE_CX_PARAM,
            'q': self.q
        }
        return '{0}?{1}'.format(search_url,
                                urllib.urlencode(search_params))

    def get_search_result(self):
        rest_url = self.get_rest_url()
        error = ''
        try:
            resp = requests.get(rest_url)
            search_result = resp.content
        except:
            error = 'Error while connecting to {0}'.format(self.service_type)
        return error, search_result


class DuckDuckGoSearchService(BaseSearchService):

    def __init__(self, q):
        self.q = q
        self.service_type = DUCK_DUCK_GO_SEARCH

    def get_rest_url(self):
        search_url = SEARCH_KEY_URL_MAP.get(self.service_type)
        search_params = {
            'q': self.q,
            'format': 'json'
        }
        return '{0}?{1}'.format(search_url,
                                urllib.urlencode(search_params))

    def get_search_result(self):
        rest_url = self.get_rest_url()
        error = ''
        try:
            resp = requests.get(rest_url)
            search_result = resp.content
        except:
            error = 'Error while connecting to {0}'.format(self.service_type)
        return error, search_result


class TwitterSearchService(BaseSearchService):

    def __init__(self, q):
        self.q = q
        self.service_type = TWITTER_SEARCH

    def get_rest_url(self):
        search_url = SEARCH_KEY_URL_MAP.get(self.service_type)
        time.sleep(2)
        search_params = {
            'q': self.q
        }
        return '{0}?{1}'.format(search_url,
                                urllib.urlencode(search_params))

    def get_search_result(self):
        rest_url = self.get_rest_url()
        consumer = oauth2.Consumer(key=TWITTER_CONSUMER_TOKEN,
                                   secret=TWITTER_CONSUMER_SECRET)
        token = oauth2.Token(key=TWITTER_ACCESS_TOKEN,
                             secret=TWITTER_ACCESS_SECRET)
        client = oauth2.Client(consumer, token)
        error = ''
        try:
            response, content = client.request(rest_url, method="GET",
                                           body="", headers=None)
            search_result = content
        except:
            error = 'Error while connecting to {0}'.format(self.service_type)
        return error, search_result
