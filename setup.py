from setuptools import setup

setup(
    name="popular-github-repo-finder",
    version="0.0.1",
    author="Lu Pan",
    author_email="panlu1412@gmail.com",
    description="A command line tool for finding popular github repos inside an org",
    license="BSD",
    install_requires=['requests >= 2.7.0'],
    py_modules=['main', 'popular_github_repo_finder'],
    packages=['github_sdk', 'utils'],
    entry_points={
        'console_scripts': [
            'popular_github_repo_finder = main:main',
        ],
    },
)
