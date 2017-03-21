
import json
import requests
import requests.exceptions

class HttpRequest(object):

    def __init__(self, url, ssl=False):
        '''
        connect to http server
        '''
        prefix = 'http'
        if ssl:
            prefix = 'https'

        self.url = url 

        self.session = requests.Session()

        self.headers = {
            'Content-type': 'application/json',
            'Accept': 'text/plain'
        }

    def request(self, method='POST', params=None, data=None,
            expected_response_code=200, sub_url=None, ping=False):
        if params is None:
            params = {}

        if isinstance(data, (dict, list)):
            data = json.dumps(data)

        if ping:
            url = self.url_ping
        elif sub_url:
            url = self.url + sub_url
        else:
            url = self.url

        # Retry 3 times if connection error
        for i in range(0, 3):
            try:
                response = self.session.request(
                        method=method,
                        url=url,
                        params=params,
                        data=data,
                        headers=self.headers
                )
                break
            except requests.exceptions.ConnectionError as e:
                if i < 2:
                    continue
                else:
                    raise KapacitorConnectionError(e)

        if response.status_code >= 500 and response.status_code < 600:
            raise HttpServerError(response.content)
        elif response.status_code == expected_response_code:
            return response
        else:
            raise HttpClientError(response.content)

    def _ping(self):
        method = 'GET'

        try:
            self.request(method=method, expected_response_code=204, ping=True)
        except HttpConnectionError as e:
            return False
        except HttpClientError as e:
            return False
        else:
            return True

    def _get(self, task_id):
        method = "GET"

        url = '/' + task_id
        result = self.request(method=method, expected_response_code=200, sub_url=url)

        return result.json()

    def _list(self):
        method = "GET"

        params = {}
        #params['viewmode'] = 'list' 

        #url = '?'
        url = ''

        result = self.request(method=method, params=params,
                              expected_response_code=200, sub_url=url)

        return result.json()

class HttpClientError(Exception):
    """Raised when an error occurs in the request."""

    def __init__(self, content):
        super(HttpClientError, self).__init__(content)

class HttpConnectionError(HttpClientError):
    """Raised when the client cannot connect to the server."""

class HttpServerError(Exception):
    """Raised when a server error occurs."""

    def __init__(self, content):
        super(HttpServerError, self).__init__(content)


h = HttpRequest('http://blog.csdn.net/ygtlovezf')

r = h._list()
print r 
