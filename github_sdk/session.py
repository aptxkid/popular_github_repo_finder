from __future__ import unicode_literals

import time

import requests

from exception import GithubAPIException


class Session(object):
    """
    Session class of the Github SDK, which is responsible of preparing each request and connection pooling.
    """

    def __init__(self, user_agent, client_id=None, client_secret=None):
        """
        :param user_agent: User-Agent string
        :type user_agent: unicode
        :param client_id: github app client id
        :type client_id: unicode
        :param client_secret: github app client secret
        :type client_secret: unicode
        """
        self._requests_session = requests.session()
        self._user_agent = user_agent
        self._client_id = client_id
        self._client_secret = client_secret

    def make_request(self, method, url, headers=None, params=None, **kwargs):
        """
        :param method: http method name (e.g. 'GET', 'POST')
        :type method: unicode
        :param url: url
        :type url: unicode
        :param headers: request headers
        :type headers: `dict`
        :return: A requests response object
        :rtype: :class:`Response`
        """
        if headers is None:
            headers = {}
        headers.update({
            'Accept': 'application/vnd.github.v3+json',
            'User-Agent': self._user_agent,
        })
        if params is None:
            params = {}
        params.update({
            'client_id': self._client_id,
            'client_secret': self._client_secret,
        })
        return self._requests_session.request(
            method=method,
            url=url,
            headers=headers,
            params=params,
            **kwargs
        )

    def request_with_automatic_retry(self, method, url, **kwargs):
        """
        Make requests with automatic retry regarding to rate limiting.

        :param method: http method name (e.g. 'GET', 'POST')
        :type method: unicode
        :param url: url
        :type url: unicode
        :return: A tuple of Json response and link headers
        :rtype: (`dict`, `dict`)
        """
        response = self.make_request(method=method, url=url, **kwargs)
        try:
            json_body = response.json()
        except ValueError:
            raise GithubAPIException(
                status=response.status_code,
                url=url,
                method=method,
                message='Invalid Json response',
                content=response.content,
            )

        if response.ok:
            return json_body, response.links
        else:
            if response.status_code == 403 and response.headers.get('X-RateLimit-Remaining') == '0':
                #handle rate limit
                reset_time = int(response.headers.get('X-RateLimit-Reset'))
                print 'reset time: {}'.format(reset_time)
                now = time.time()
                print 'now: {}'.format(now)
                if now < reset_time:
                    print 'sleeping for {} seconds'.format(reset_time - now)
                    time.sleep(reset_time - now)
                return self.request_with_automatic_retry(method=method, url=url)

            else:
                raise GithubAPIException(
                    status=response.status_code,
                    url=url,
                    method=method,
                    message=json_body.get('message'),
                    content=response.content,
                    headers=response.headers,
                )

    def get_all(self, url):
        """
        Get all the resources from url. This method will follow the link headers and iterate through all the pages
        to get all the resources.
        :param url: The url of the resources
        :type url: unicode
        :return: A json response including all the resources
        :rtype: `dict`
        """
        json_result, links = self.request_with_automatic_retry(method='GET', url=url)

        while links and 'next' in links and 'url' in links['next']:
            paging_json_result, paging_links = self.request_with_automatic_retry(method='GET', url=links['next']['url'])
            json_result.extend(paging_json_result)
            links = paging_links

        return json_result
