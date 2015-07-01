# Popular Github Repo Finder

## Install
``` bash
make install
```

## Usage
``` bash

usage: popular_github_repo_finder [-h] --org ORG -n N [--output OUTPUT]
                                  [--timeout TIMEOUT] [--client_id CLIENT_ID]
                                  [--client_secret CLIENT_SECRET]

optional arguments:
  -h, --help            show this help message and exit
  --org ORG             github organization name
  -n N                  number of top repos of the org
  --output OUTPUT       sys path for writing the final result to
  --timeout TIMEOUT     specify a timeout. If the command does not finish
                        within the timeout it would be killed.
  --client_id CLIENT_ID
                        Github application client id. Pass this in with
                        --client_secret to have a higher rate limiting
  --client_secret CLIENT_SECRET
                        Github application client secret. Pass this in with
                        --client_id to have a higher rate limiting

```

## Example
``` bash
popular_github_repo_finder --org box -n 1 --client_id YOU_GITHUB_APP_CLIENT_ID --client_secret YOUR_GITHUB_APP_CLIENT_SECRET

{   u'n': 1,
    u'note': u'contribution_percentage == -1 means the repo has zero fork',
    u'org': u'box',
    u'top_n_by_contribution_percentage': [   {   u'contribution_percentage': 12.916666666666666,
                                                 u'full_name': u'box/ClusterRunner',
                                                 u'number_of_forks': 12,
                                                 u'number_of_pull_requests': 155,
                                                 u'number_of_stars': 55,
                                                 u'repo_id': 25371175,
                                                 u'url': u'https://github.com/box/ClusterRunner'}],
    u'top_n_by_forks': [   {   u'contribution_percentage': 0.3467741935483871,
                               u'full_name': u'box/Anemometer',
                               u'number_of_forks': 124,
                               u'number_of_pull_requests': 43,
                               u'number_of_stars': 617,
                               u'repo_id': 3812233,
                               u'url': u'https://github.com/box/Anemometer'}],
    u'top_n_by_pull_requests': [   {   u'contribution_percentage': 3.537037037037037,
                                       u'full_name': u'box/deprecated-box-java-sdk-v2',
                                       u'number_of_forks': 54,
                                       u'number_of_pull_requests': 191,
                                       u'number_of_stars': 89,
                                       u'repo_id': 9204340,
                                       u'url': u'https://github.com/box/deprecated-box-java-sdk-v2'}],
    u'top_n_by_stars': [   {   u'contribution_percentage': 0.36633663366336633,
                               u'full_name': u'box/t3js',
                               u'number_of_forks': 101,
                               u'number_of_pull_requests': 37,
                               u'number_of_stars': 1361,
                               u'repo_id': 33621458,
                               u'url': u'https://github.com/box/t3js'}]}

```

## Help

You can register your Github app here https://github.com/settings/applications/new
