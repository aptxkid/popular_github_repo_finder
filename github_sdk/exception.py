from __future__ import unicode_literals


class BaseGithubException(Exception):
    def __str__(self):
        return self.__unicode__().encode('utf-8')


class GithubAPIException(BaseGithubException):
    def __init__(self, status, url, method, headers=None, message=None, content=None):
        self._status = status
        self._url = url
        self._method = method
        self._headers = headers
        self._message = message
        self._content = content

    def __unicode__(self):
        return 'Status: {}\nurl: {}\nmethod: {}\nheaders: {}\nmessage: {}\ncontent: {}\n'.format(
            self._status,
            self._url,
            self._method,
            self._headers,
            self._message,
            self._content,
        )
