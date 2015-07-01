from __future__ import unicode_literals

from argparse import ArgumentParser
import json
import logging
import os
import pprint
import signal
import time
import threading
from threading import Event

from popular_github_repo_finder import PopularGithubRepoFinder
from utils import log, unhandled_exception_handler


log.LOG_FILE_NAME = 'popular_github_repo_finder.log'
unhandled_exception_handler.configure_unhandled_exception_handler()
logger = log.get_logger('main')


def _parse_args():
    parser = ArgumentParser()
    parser.add_argument(
        '--org',
        type=unicode,
        required=True,
        help='github organization name',
    )
    parser.add_argument(
        '-n',
        type=int,
        required=True,
        help='number of top repos of the org',
    )
    parser.add_argument(
        '--output',
        type=unicode,
        required=False,
        help='sys path for writing the final result to',
    )
    parser.add_argument(
        '--timeout',
        type=int,
        required=False,
        help='specify a timeout. If the command does not finish within the timeout it would be killed.',
    )
    parser.add_argument(
        '--client_id',
        type=unicode,
        required=False,
        help='Github application client id. Pass this in with --client_secret to have a higher rate limiting',
    )
    parser.add_argument(
        '--client_secret',
        type=unicode,
        required=False,
        help='Github application client secret. Pass this in with --client_id to have a higher rate limiting',
    )
    args_dict = vars(parser.parse_args())

    return args_dict


def _start_timer(timeout, completed_event):
    if not timeout:
        return

    def timer():
        deadline = time.time() + timeout
        while time.time() < deadline and not completed_event.is_set():
            time.sleep(1)
        logger.warn('Timeout {} seconds has been reached. Killing the process.'.format(timeout))
        os.kill(os.getpid(), signal.SIGKILL)

    logger.info('Starting timer for {} seconds'.format(timeout))
    timer_thread = threading.Thread(target=timer)
    timer_thread.start()


def main():
    args = _parse_args()
    completed_event = Event()
    _start_timer(args['timeout'], completed_event)
    logger.info('Starting up!')
    finder = PopularGithubRepoFinder(
        org=args['org'],
        client_id=args['client_id'],
        client_secret=args['client_secret'],
    )

    logger.info('Generating report')

    report = {
        'org': args['org'],
        'n': args['n'],
        'note': 'contribution_percentage == -1 means the repo has zero fork',
        'top_n_by_stars': finder.top_n_by_stars_count(args['n']),
        'top_n_by_forks': finder.top_n_by_forks_count(args['n']),
        'top_n_by_pull_requests': finder.top_n_by_pull_requests_count(args['n']),
        'top_n_by_contribution_percentage': finder.top_n_by_contribution_percentage(args['n']),
    }

    if args['output']:
        with open(args['output'], 'w') as output_file:
            json.dump(report, output_file)
    else:
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(report)

    logger.info('Report generated')

    completed_event.set()
    logging.shutdown()


if __name__ == '__main__':
    main()
