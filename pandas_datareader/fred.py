from pandas_datareader.compat import is_list_like
import pandas as pd
import requests
from pandas import concat, read_csv
from pandas_datareader.base import _BaseReader

import os
import json
import functools
from ._utils import run_tasks_in_parallel

def get_fred_api(tmp_cache=True):
    filename = os.path.expanduser('~/.cred/fred/cred.json')
    if os.path.exists(filename):
        api_key = json.load(open(filename))['API_KEY']
    else:
        api_key = os.environ['FRED_API_KEY']
    # do not use fredapi it is incomplete
    # use: pip install FRB
    from fred import Fred
    if api_key is None:
        raise Exception("no .cred/fred/cred.json['API_KEY'] or environ FRED_API_KEY found! Get one by signing up at the fred site.")
    fred = Fred(api_key=api_key)
    return fred

def offset_paginator(fun, limit=1000):
    """
    fun(offset, limit)
    """
    limit = min(limit, 1000)
    # pretty awful
    offset = 0
    n = 20
    res = list()
    while True:
        offsets = range(offset, offset + limit * n, limit)
        print(offsets)
        tasks = [functools.partial(fun, o, limit) for o in offsets]
        r = run_tasks_in_parallel(*tasks, max_workers=max(n, 20))
        good = [x for x in r if x['exception'] is None]
        good = [x['result'] for x in good if x['result'].shape[0] > 0]
        res.extend(good)
        if len(good) < len(r):
            # stop when first encountering not all-perfect run
            break
        offset += limit * n
    df = pd.concat(res, sort=False)
    return df

def get_series_by_tag(tag='daily'):
    """
    use ; separated list for many I think
    attempts to paginate with some degree of parallism in chunks
    """
    fred = get_fred_api()
    def fun(offset, limit):
        print('getting {} {} for tag {}'.format(offset, limit, tag))
        return fred.tag.series(tag, response_type='df', params=dict(offset=offset, limit=limit))
    return offset_paginator(fun)

class FredReader(_BaseReader):
    """
    Get data for the given name from the St. Louis FED (FRED).
    """

    @property
    def url(self):
        """API URL"""
        return "https://fred.stlouisfed.org/graph/fredgraph.csv"

    def read(self):
        """Read data

        Returns
        -------
        data : DataFrame
            If multiple names are passed for "series" then the index of the
            DataFrame is the outer join of the indicies of each series.
        """
        try:
            return self._read()
        finally:
            self.close()

    def _read(self):
        if not is_list_like(self.symbols):
            names = [self.symbols]
        else:
            names = self.symbols

        urls = ["{}?id={}".format(self.url, n) for n in names]

        def fetch_data(url, name):
            """Utillity to fetch data"""
            resp = self._read_url_as_StringIO(url)
            data = read_csv(resp, index_col=0, parse_dates=True,
                            header=None, skiprows=1, names=["DATE", name],
                            na_values='.')
            try:
                return data.truncate(self.start, self.end)
            except KeyError:  # pragma: no cover
                if data.iloc[3].name[7:12] == 'Error':
                    raise IOError("Failed to get the data. Check that "
                                  "{0!r} is a valid FRED series.".format(name))
                raise
        df = concat([fetch_data(url, n) for url, n in zip(urls, names)],
                    axis=1, join='outer')
        return df

    def get_available_datasets(self):
        # or get_series_by_tag('daily;weekly;monthly;quarterly;annual')
        # for k in ['daily', 'weekly', 'monthly', 'quarterly', 'annual']:
        dfs = list()
        for k in ['daily', 'weekly', 'monthly', 'annual']:
            df = get_series_by_tag(k)
            df['tag'] = k
            dfs.append(df)
        df = pd.concat(dfs, axis=0, sort=False)
        return df
