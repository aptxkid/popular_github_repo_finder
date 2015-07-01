from __future__ import unicode_literals

import heapq

from github_sdk.client import Client

from utils import log


class PopularGithubRepoFinder(object):
    """
    Popular github repo finder is a class responsible of finding popular github repos inside a github organization.
    """

    def __init__(self, org, client_id=None, client_secret=None):
        """
        :param org: github org name
        :type org: unicode
        :param client_id: github app client id
        :type client_id: unicode
        :param client_secret: github app client secret
        :type client_secret: unicode
        """
        self._logger = log.get_logger('PopularGithubRepoFinder')
        self._client = Client(
            user_agent='popular-github-repo-finder',
            client_id=client_id,
            client_secret=client_secret,
        )
        self._org = org
        self._all_repos = self._get_all_repos()

    def _get_all_repos(self):
        self._logger.info('Making API calls to get all the repo info')
        all_repos = self._client.repos(org=self._org)
        self._logger.info('All repos returned from API:\n%s', format(all_repos))
        return all_repos

    def _top_n(self, n, key):
        top_repos = heapq.nlargest(n, self._all_repos, key=key)

        return [
            {
                'repo_id': r.repo_id,
                'full_name': r.name,
                'url': r.url,
                'number_of_stars': r.number_of_stars,
                'number_of_forks': r.number_of_forks,
                'number_of_pull_requests': len(r.pull_requests),
                'contribution_percentage': len(r.pull_requests)/float(r.number_of_forks) if r.number_of_forks > 0 else -1
            } for r in top_repos
        ]

    def top_n_by_stars_count(self, n):
        """
        Get top N repos by the stars count.
        :param n: Number of top starred repos to be returned
        :type n: int
        :return: a list of at most N repos with most stars inside the org
        :rtype: [`dict`]
        """
        return self._top_n(n, key=lambda r: r.number_of_stars)

    def top_n_by_forks_count(self, n):
        """
        Get top N repos by the forks count.
        :param n: Number of the top forked repos to be returned
        :type n: int
        :return: a list of at most N repos with most forks inside the org
        :rtype: [`dict`]
        """
        return self._top_n(n, key=lambda r: r.number_of_forks)

    def top_n_by_pull_requests_count(self, n):
        """
        Get top N repos by the pull requests count.
        :param n: Number of repos with the most pull requests inside the org
        :type n: int
        :return: a list of at most N repos with most pull requests inside the org
        :rtype: [`dict`]
        """
        return self._top_n(n, key=lambda r: len(r.pull_requests))

    def top_n_by_contribution_percentage(self, n):
        """
        Get top N repos by the contribution percentage defined by PRs/#forks.
        :param n: Number of repos with the biggest contribution percentage
        :type n: int
        :return: a list of at most N repos with largest contribution percentage inside the org
        :rtype: [`dict`]
        """
        def get_contribution_percentage(repo):
            if repo.number_of_forks > 0:
                return len(repo.pull_requests) / float(repo.number_of_forks)
            else:
                return -1
        return self._top_n(n, key=get_contribution_percentage)

