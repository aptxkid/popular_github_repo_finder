from __future__ import unicode_literals

import math
import unittest

from mock import Mock, patch

from github_sdk.repo import Repo
from popular_github_repo_finder import PopularGithubRepoFinder


class TestPopularGithubRepoFinder(unittest.TestCase):

    def setUp(self):
        super(TestPopularGithubRepoFinder, self).setUp()

        # patch Client in popular_github_repo_finder module
        patcher = patch('popular_github_repo_finder.Client', autospec=True)
        MockClient = patcher.start()
        mock_client_instance = MockClient('some_org')
        MockClient.return_value = mock_client_instance

        mock_repos = [
            # most starred
            self._get_fake_repo(
                name='some_org/repo_1',
                repo_id='1111',
                url='https://github.com/some_org/repo_1',
                number_of_stars=1000,
                number_of_forks=0,
                number_of_pull_requests=20,
            ),
            # most forked
            self._get_fake_repo(
                name='some_org/repo_2',
                repo_id='2222',
                url='https://github.com/some_org/repo_2',
                number_of_stars=20,
                number_of_forks=1000,
                number_of_pull_requests=0,
            ),
            # most pull requests
            self._get_fake_repo(
                name='some_org/repo_3',
                repo_id='3333',
                url='https://github.com/some_org/repo_3',
                number_of_stars=0,
                number_of_forks=20,
                number_of_pull_requests=1000,
            ),
            # most contributed
            self._get_fake_repo(
                name='some_org/repo_4',
                repo_id='4444',
                url='https://github.com/some_org/repo_4',
                number_of_stars=0,
                number_of_forks=1,
                number_of_pull_requests=1000,
            ),
        ]
        mock_client_instance.repos.return_value = mock_repos

        self._finder = PopularGithubRepoFinder('fake_org')

    def _get_fake_repo(self, name, repo_id, url, number_of_stars, number_of_forks, number_of_pull_requests):
        repo = Mock(Repo)
        repo.name = name
        repo.repo_id = repo_id
        repo.url = url
        repo.number_of_stars = number_of_stars
        repo.number_of_forks = number_of_forks
        repo.pull_requests = [{}] * number_of_pull_requests
        return repo

    def _assert_equal_results(self, expected_repos, actual_repos):
        self.assertEqual(len(expected_repos), len(actual_repos))
        for i in range(len(expected_repos)):
            self.assertEqual(expected_repos[i], actual_repos[i])

    def test_top_n_by_star_counts(self):
        top_n_by_star_counts = self._finder.top_n_by_stars_count(1)
        self._assert_equal_results(
            [{
                'repo_id': '1111',
                'full_name': 'some_org/repo_1',
                'url': 'https://github.com/some_org/repo_1',
                'number_of_stars': 1000,
                'number_of_forks': 0,
                'number_of_pull_requests': 20,
                'contribution_percentage': -1,
            }],
            top_n_by_star_counts,
        )

    def test_top_n_by_fork_counts(self):
        top_n_by_fork_counts = self._finder.top_n_by_forks_count(1)
        self._assert_equal_results(
            [{
                'repo_id': '2222',
                'full_name': 'some_org/repo_2',
                'url': 'https://github.com/some_org/repo_2',
                'number_of_stars': 20,
                'number_of_forks': 1000,
                'number_of_pull_requests': 0,
                'contribution_percentage': 0.0,
            }],
            top_n_by_fork_counts,
        )

    def test_top_n_by_number_of_pull_requests(self):
        top_n_by_pull_requests = self._finder.top_n_by_pull_requests_count(1)
        self._assert_equal_results(
            [{
                'repo_id': '3333',
                'full_name': 'some_org/repo_3',
                'url': 'https://github.com/some_org/repo_3',
                'number_of_stars': 0,
                'number_of_forks': 20,
                'number_of_pull_requests': 1000,
                'contribution_percentage': 50.0,
            }],
            top_n_by_pull_requests,
        )

    def test_top_n_by_contribution_percentage(self):
        top_n_by_contribution_percentage = self._finder.top_n_by_contribution_percentage(1)
        self._assert_equal_results(
            [{
                'repo_id': '4444',
                'full_name': 'some_org/repo_4',
                'url': 'https://github.com/some_org/repo_4',
                'number_of_stars': 0,
                'number_of_forks': 1,
                'number_of_pull_requests': 1000,
                'contribution_percentage': 1000.0,
            }],
            top_n_by_contribution_percentage,
        )
