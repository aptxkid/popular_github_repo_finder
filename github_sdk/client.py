from __future__ import unicode_literals


from api import API
from github_sdk.repo import Repo
from session import Session


class Client(object):
    """
    Github SDK client. This is the entry point of all Github interactions.
    """

    def __init__(self, user_agent, client_id=None, client_secret=None):
        """
        :param user_agent:  User-Agent string
        :type user_agent: unicode
        :param client_id: github app client id
        :type client_id: unicode
        :param client_secret: github app client secret
        :type client_secret: unicode
        """
        self._session = Session(user_agent, client_id, client_secret)

    def _repo_translator(self, repos_in_json):
        return [Repo(
                session=self._session,
                repo_id=r['id'],
                name=r['full_name'],
                url=r['html_url'],
                number_of_forks=r['forks_count'],
                number_of_stars=r['stargazers_count'],
                ) for r in repos_in_json]

    def repos(self, org):
        """
        Get all the repos for organization.
        :param org: the name of the organization to get all the repos from
        :type org: unicode
        :return: A list of Repo objects inside the org
        :rtype: [:class:`Repo`]
        """
        url = '{}/orgs/{}/repos'.format(
            API.BASE_ENDPOINT,
            org,
        )
        return self._repo_translator(self._session.get_all(url))
