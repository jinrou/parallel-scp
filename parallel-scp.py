#! /usr/bin/env python
# -*- coding: utf-8 -*-


from multiprocessing.dummy import Pool as ThreadPool
import subprocess

import sys
import getpass
import click
import logging

LOG = logging.getLogger()


def run_cmd(cmd):
    LOG.debug(cmd)
    subprocess.check_output(cmd)


def task_list(user, src, dst):
    tasks = []
    for host in sys.stdin:
        full_dst = "{}@{}:{}".format(user, host.strip(), dst)
        cmd = ["/usr/bin/scp", src, full_dst]
        tasks.append(cmd)
    return tasks


@click.command()
@click.argument('src', nargs=1)
@click.argument('dst', nargs=1)
@click.argument('user', nargs=1)
def main(src, dst, user):
    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)
    src = sys.argv[1]
    dst = sys.argv[2]
    user = None
    if len(sys.argv) > 3:
        user = sys.argv[3]
    else:
        user = getpass.getuser()

    pool = ThreadPool(10)
    pool.map(run_cmd, task_list(user, src, dst))


if __name__ == '__main__':
    main()
