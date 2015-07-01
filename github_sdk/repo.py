from __future__ import unicode_literals

from multiprocessing.pool import ThreadPool

from api import API


class Repo(object):
    """
    Represents a Github repo.
    """

    thread_pool = ThreadPool(processes=4)

    def __init__(self, session, repo_id, name, url, number_of_stars, number_of_forks):
        """
        :param session: requests session for making requests
        :type session: :class:`Session`
        :param repo_id: github repo id
        :type repo_id: int
        :param name: github repo name
        :type name: unicode
        :param url: github repo url
        :type url: unicode
        :param number_of_stars: number of stars on the repo
        :type number_of_stars: int
        :param number_of_forks: number of forks on the repo
        :type number_of_forks: int
        """
        self._session = session
        self._repo_id = repo_id
        self._name = name
        self._url = url
        self._number_of_stars = number_of_stars
        self._number_of_forks = number_of_forks
        self._promise = self.thread_pool.apply_async(self._get_all_pull_requests)

    @property
    def name(self):
        return self._name

    @property
    def repo_id(self):
        return self._repo_id

    @property
    def url(self):
        return self._url

    @property
    def number_of_stars(self):
        return self._number_of_stars

    @property
    def number_of_forks(self):
        return self._number_of_forks

    def _get_all_pull_requests(self):
        url = '{}/repos/{}/pulls?state=all'.format(
            API.BASE_ENDPOINT,
            self._name,
        )
        self._pull_requests = self._session.get_all(url)

    @property
    def pull_requests(self):
        self._promise.get()
        return self._pull_requests

