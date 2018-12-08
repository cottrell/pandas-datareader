import importlib
import logging
from ._version import get_versions
from .data import (DataReader, Options, get_components_yahoo,
                   get_dailysummary_iex, get_data_enigma, get_data_famafrench,
                   get_data_fred, get_data_google, get_data_moex,
                   get_data_morningstar, get_data_quandl, get_data_stooq,
                   get_data_yahoo, get_data_yahoo_actions, get_iex_book,
                   get_iex_symbols, get_last_iex, get_markets_iex,
                   get_nasdaq_symbols,
                   get_quote_google, get_quote_yahoo, get_recent_iex,
                   get_records_iex, get_summary_iex, get_tops_iex,
                   get_data_tiingo, get_data_alphavantage)

__version__ = get_versions()['version']
del get_versions

__all__ = ['__version__', 'get_components_yahoo', 'get_data_enigma',
           'get_data_famafrench', 'get_data_google', 'get_data_yahoo',
           'get_data_yahoo_actions', 'get_quote_google', 'get_quote_yahoo',
           'get_iex_book', 'get_iex_symbols', 'get_last_iex',
           'get_markets_iex', 'get_recent_iex', 'get_records_iex',
           'get_summary_iex', 'get_tops_iex',
           'get_nasdaq_symbols', 'get_data_quandl', 'get_data_moex',
           'get_data_fred', 'get_dailysummary_iex', 'get_data_morningstar',
           'get_data_stooq', 'DataReader', 'Options',
           'get_data_tiingo', 'get_data_alphavantage']

# git grep '^class [^_].*Reader.*' | grep -v Test | sed -e 's/\.py:class /,/' -e 's/://' -e 's/\/__init__//' -e 's/\//./g' -e 's/(/,/' -e 's/)//'
_sources_list = """\
av,AlphaVantage,_BaseReader
av.forex,AVForexReader,AlphaVantage
av.quotes,AVQuotesReader,AlphaVantage
av.sector,AVSectorPerformanceReader,AlphaVantage
av.time_series,AVTimeSeriesReader,AlphaVantage
bankofcanada,BankOfCanadaReader,_BaseReader
enigma,EnigmaReader,_BaseReader
eurostat,EurostatReader,_BaseReader
famafrench,FamaFrenchReader,_BaseReader
fred,FredReader,_BaseReader
google.daily,GoogleDailyReader,_DailyBaseReader
google.options,Options,_OptionBaseReader
google.quotes,GoogleQuotesReader,_BaseReader
iex,IEX,_BaseReader
iex.daily,IEXDailyReader,_DailyBaseReader
iex.market,MarketReader,IEX
iex.ref,SymbolsReader,IEX
iex.stats,DailySummaryReader,IEX
iex.stats,MonthlySummaryReader,IEX
iex.stats,RecordsReader,IEX
iex.stats,RecentReader,IEX
iex.tops,TopsReader,IEX
iex.tops,LastReader,IEX
moex,MoexReader,_DailyBaseReader
mstar.daily,MorningstarDailyReader,_BaseReader
oecd,OECDReader,_BaseReader
quandl,QuandlReader,_DailyBaseReader
robinhood,RobinhoodQuoteReader,_BaseReader
robinhood,RobinhoodHistoricalReader,RobinhoodQuoteReader
stooq,StooqDailyReader,_DailyBaseReader
tiingo,TiingoDailyReader,_BaseReader
tiingo,TiingoMetaDataReader,TiingoDailyReader
tiingo,TiingoQuoteReader,TiingoDailyReader
tsp,TSPReader,_BaseReader
wb,WorldBankReader,_BaseReader
yahoo.actions,YahooActionReader,YahooDailyReader
yahoo.actions,YahooDivReader,YahooActionReader
yahoo.actions,YahooSplitReader,YahooActionReader
yahoo.daily,YahooDailyReader,_DailyBaseReader
yahoo.fx,YahooFXReader,YahooDailyReader
yahoo.options,Options,_OptionBaseReader
yahoo.quotes,YahooQuotesReader,_BaseReader"""


class _ReaderHelper():
    def __init__(self):
        self._setup_readers()
    def _setup_readers(self):
        sources = [x.split(',') for x in _sources_list.split()]
        no_symbols = ''
        self._readers = list()
        for [name, class_, base] in sources:
            mod = importlib.import_module('pandas_datareader.' + name)
            local_name = (name + '.' + class_).replace('.', '_')
            try:
                reader = mod.__dict__[class_](no_symbols)
                self._readers.append(local_name)
                setattr(self, local_name, reader)
            except Exception as e:
                logging.debug('skipping reader {}:{} due to error: {}'.format(name, class_, e))
                # raise e
                continue
    def __repr__(self):
        return self.__class__.__name__ + '\n\t.' + '\n\t.'.join(self._readers)

helper = _ReaderHelper()
