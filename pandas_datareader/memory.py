import os
import sys
import requests
from joblib import Memory
import superbasic # registers new store_backend

_mydir = os.path.dirname(__file__)
_pandas_dataread_dir = os.path.expanduser('~/.pandas_datareader/')
_joblib_cache = os.path.join(_pandas_dataread_dir, 'joblib_cache')
memory = Memory(_joblib_cache, verbose=1)

# not really using this has_joblib
def has_joblib():
    if has_joblib._has_joblib is None:
        try:
            import joblib
            has_joblib._has_joblib = True
        except ModuleNotFoundError as e:
            print('joblib is not installed, you will not be able to use optional joblib caching.')
            has_joblib._has_joblib = False
    return has_joblib._has_joblib
has_joblib._has_joblib = None

@memory.cache
def cached_requests_get(url, return_these=['text'], params=None, **kwargs):
    res = requests.get(url, params=params, **kwargs)
    if not res.ok:
        raise Exception('ERROR getting {}: {}'.format(url, r.reason))
    return {k: getattr(res, k) for k in return_these}
