pandas-datareader
=================

Up to date remote data access for pandas, works for multiple versions of pandas.

.. image:: https://img.shields.io/pypi/v/pandas-datareader.svg
    :target: https://pypi.python.org/pypi/pandas-datareader/

.. image:: https://travis-ci.org/pydata/pandas-datareader.svg?branch=master
    :target: https://travis-ci.org/pydata/pandas-datareader

.. image:: https://coveralls.io/repos/pydata/pandas-datareader/badge.svg?branch=master
    :target: https://coveralls.io/r/pydata/pandas-datareader

.. image:: https://readthedocs.org/projects/pandas-datareader/badge/?version=latest
    :target: https://pandas-datareader.readthedocs.io/en/latest/

.. image:: https://landscape.io/github/pydata/pandas-datareader/master/landscape.svg?style=flat
   :target: https://landscape.io/github/pydata/pandas-datareader/master
   :alt: Code Health

.. warning::

   As of v0.7.0 Google finance and Morningstar have been been immediately deprecated due to
   large changes in their API and no stable replacement.


Usage
-----

Starting in 0.19.0, pandas no longer supports ``pandas.io.data`` or ``pandas.io.wb``, so
you must replace your imports from ``pandas.io`` with those from ``pandas_datareader``:

.. code-block:: python

   from pandas.io import data, wb # becomes
   from pandas_datareader import data, wb

Many functions from the data module have been included in the top level API.

.. code-block:: python

   import pandas_datareader as pdr
   pdr.get_data_fred('GS10')

Documentation
-------------

`Stable documentation <https://pydata.github.io/pandas-datareader/stable/>`__
is available on
`github.io <https://pydata.github.io/pandas-datareader/stable/>`__.
A second copy of the stable documentation is hosted on
`read the docs <https://pandas-datareader.readthedocs.io/>`_ for more details.

`Development documentation <https://pydata.github.io/pandas-datareader/devel/>`__
is available for the latest changes in master.

Installation
------------

Requirements
~~~~~~~~~~~~

Using pandas datareader requires the following packages:

* pandas>=0.19.2
* lxml
* requests>=2.3.0
* wrapt

Building the documentation additionally requires:

* matplotlib
* ipython
* sphinx
* sphinx_rtd_theme

Testing requires pytest.

Install latest release version via pip
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: shell

   $ pip install pandas-datareader

Install latest development version
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: shell

    $ pip install git+https://github.com/pydata/pandas-datareader.git

or

.. code-block:: shell

    $ git clone https://github.com/pydata/pandas-datareader.git
    $ python setup.py install


New Workflow/API via helper and get_available_datasets
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    In [1]: import pandas_datareader as pdr

    In [2]: pdr.helper
    Out[2]:
    _ReaderHelper
    	.bankofcanada_BankOfCanadaReader
    	.eurostat_EurostatReader
    	.famafrench_FamaFrenchReader
    	.fred_FredReader
    	.google_options_Options
    	.google_quotes_GoogleQuotesReader
    	.iex_IEX
    	.iex_daily_IEXDailyReader
    	.iex_market_MarketReader
    	.iex_ref_SymbolsReader
    	.iex_stats_DailySummaryReader
    	.iex_stats_MonthlySummaryReader
    	.iex_stats_RecordsReader
    	.iex_stats_RecentReader
    	.iex_tops_TopsReader
    	.iex_tops_LastReader
    	.moex_MoexReader
    	.oecd_OECDReader
    	.robinhood_RobinhoodQuoteReader
    	.robinhood_RobinhoodHistoricalReader
    	.stooq_StooqDailyReader
    	.tsp_TSPReader
    	.wb_WorldBankReader
    	.yahoo_actions_YahooActionReader
    	.yahoo_actions_YahooDivReader
    	.yahoo_actions_YahooSplitReader
    	.yahoo_daily_YahooDailyReader
    	.yahoo_fx_YahooFXReader
    	.yahoo_options_Options
    	.yahoo_quotes_YahooQuotesReader

    In [3]: d = pdr.helper.yahoo_daily_YahooDailyReader.get_available_datasets()

    In [4]: df = pdr.helper.yahoo_daily_YahooDailyReader.get_symbols('goog')

    In [5]: df.shape
    Out[5]: (2253, 6)


Fred tag searches
~~~~~~~~~~~~~~~~~

Some starting points for crawling the Fred API.

Note you can still get Fred data from Quandl for free. Not sure if that will change with the recent aquisition.

.. code-block:: python

        In [10]: import pandas_datareader.fred as fred

        In [11]: d = fred.get_series_by_tag('daily;rate')
        range(0, 20000, 1000)
        getting 0 1000 for tag daily;rate
        getting 1000 1000 for tag daily;rate
        getting 2000 1000 for tag daily;rate
        getting 3000 1000 for tag daily;rate
        getting 4000 1000 for tag daily;rate
        getting 5000 1000 for tag daily;rate
        getting 6000 1000 for tag daily;rate
        getting 7000 1000 for tag daily;rate
        getting 8000 1000 for tag daily;rate
        getting 9000 1000 for tag daily;rate
        getting 10000 1000 for tag daily;rate
        getting 11000 1000 for tag daily;rate
        getting 12000 1000 for tag daily;rate
        getting 13000 1000 for tag daily;rate
        getting 14000 1000 for tag daily;rate
        getting 15000 1000 for tag daily;rate
        getting 16000 1000 for tag daily;rate
        getting 17000 1000 for tag daily;rate
        getting 18000 1000 for tag daily;rate
        getting 19000 1000 for tag daily;rate

        In [12]: d.head().T.head().T
        Out[12]:
          frequency frequency_short group_popularity           id         last_updated
        0     Daily               D               69       AAA10Y  2018-12-13 21:51:03
        1     Daily               D               43        AAAFF  2018-12-13 21:51:13
        2     Daily               D                1  AB1020AAAMT  2018-12-13 15:11:03
        3     Daily               D                1  AB1020AAVOL  2018-12-13 15:11:03
        4     Daily               D                1    AB14AAAMT  2018-12-13 15:11:03

        In [13]: d.shape
        Out[13]: (471, 16)


