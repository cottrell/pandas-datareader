import datetime as dt
import os
import subprocess
import requests
from pandas import to_datetime
from pandas_datareader.compat import is_number
import functools
import concurrent
import collections
import importlib
import logging


def module_from_file(filename):
    module_name = os.path.basename(filename).replace('.py', '')
    spec = importlib.util.spec_from_file_location(module_name, filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

_config_filename = os.path.expanduser('~/.pandas_datareader/config.py')

def get_config():
    # TODO: flag for rate limit as well
    config_with_defaults = {'use_joblib_cache': False, 'use_ratelimit': True, 'ratelimit_period_seconds': 3600 * 2, 'ratelimit_calls': 2000}
    if os.path.exists(_config_filename):
        config = module_from_file(_config_filename)
        for k in config_with_defaults:
            if k in config.__dict__:
                config_with_defaults[k] = config.__dict__[k]
                logging.warn('INFO: using non-default {}={} from {}'.format(k, config.__dict__[k], _config_filename))
    C = collections.namedtuple('pandas_datareader_config', ['use_joblib_cache', 'use_ratelimit', 'ratelimit_period_seconds', 'ratelimit_calls'])
    d = C(**config_with_defaults)
    if not d.use_ratelimit:
        logging.warn("You are have not enabled the request ratelimit. This might lead to blocking access to sites.")
    return d

config = get_config()

class SymbolWarning(UserWarning):
    pass


class RemoteDataError(IOError):
    pass


def _sanitize_dates(start, end):
    """
    Return (datetime_start, datetime_end) tuple
    if start is None - default is 2010/01/01
    if end is None - default is today
    """
    if is_number(start):
        # regard int as year
        start = dt.datetime(start, 1, 1)
    start = to_datetime(start)

    if is_number(end):
        end = dt.datetime(end, 1, 1)
    end = to_datetime(end)

    if start is None:
        start = dt.datetime(2010, 1, 1)
    if end is None:
        end = dt.datetime.today()
    if start > end:
        raise ValueError('start must be an earlier date than end')
    return start, end


def _init_session(session, retry_count=3):
    if session is None:
        session = requests.Session()
        # do not set requests max_retries here to support arbitrary pause
    return session


# parallization/async tools
def _wrapped_errors(task):
    @functools.wraps(task)
    def inner():
        exception = None
        result = None
        try:
            result = task()
        except Exception as e:
            exception = e
        return dict(exception=exception, result=result)
    return inner


def run_tasks_in_parallel(*tasks, max_workers=10, wait=True, raise_exceptions=False):
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=max_workers)
    if not raise_exceptions:
        tasks = map(_wrapped_errors, tasks)
    fut = [executor.submit(task) for task in tasks]
    if wait:
        return [x.result() for x in fut]
    else:
        return fut


# also see _version.py
def run_command_get_output(cmd, shell=True, splitlines=True):
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=shell)
    out, err = p.communicate()
    status = p.returncode
    out = out.decode()
    err = err.decode()
    if splitlines:
        out = out.split('\n')
        err = err.split('\n')
    return dict(out=out, err=err, status=status)

def squish(gen):
    """ uniquify list preserve order """
    seen = set()
    for x in gen:
        if x not in seen and not seen.add(x):
            yield x
