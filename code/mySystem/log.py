"Logging functions for my test system."

import logging
from logging import Logger
import time
import os

# default format: '%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s'
LOGMSGFORMAT = '%(asctime)s - %(levelname)s: %(message)s'
# log level names
LEVELS = { 'debug': logging.DEBUG,
           'info': logging.INFO,
           'warning': logging.WARNING,
           'warn': logging.WARNING,
           'error': logging.ERROR,
           'critical': logging.CRITICAL }
# change this to logging.INFO to get printouts
LOGLEVELDEFAULT = logging.WARNING

class SysLogger(Logger, object):
    """My system logger
        Enable each sys .py file to with one import
        from log import [lg, info, error, warn, ...]"""

    def __init__(self, name="system"):

        Logger.__init__(self, name)

        # create console handler for write log file
        rq = time.strftime('%Y%m%d%H%M', time.localtime(time.time()))
        log_path = os.path.join(os.getcwd(), 'logs')
        logfile = os.path.join(log_path, '%s.log' % rq)
        ch = logging.FileHandler(logfile, mode='w', encoding='UTF-8')
        # create formatter
        formatter = logging.Formatter(LOGMSGFORMAT)
        # add formatter to ch
        ch.setFormatter(formatter)
        # add ch to lg and initilize log level
        self.addHandler(ch)
        self.ch = ch
        self.setLogLevel()

    def setLogLevel(self, levelname=None):
        """Setup log level.
            level name from LEVELS"""
        if levelname and levelname not in LEVELS:
            print(LEVELS)
            raise Exception( 'setLogLevel: unknown levelname %s' % levelname )
        level = LEVELS.get(levelname, LOGLEVELDEFAULT)
        self.setLevel(level)
        self.ch.setLevel(level)

# Make things a bit more convenient by adding aliases
# (info, warn, error, debug) and allowing info( 'this', 'is', 'OK' )
def makeListCompatible(fn):
    """Return a new function allowing fn( 'a 1 b' ) to be called as
       newfn( 'a', 1, 'b' )"""
    def newfn( *args ):
        "Generated function. Closure-ish."
        if len( args ) == 1:
            return fn( *args )
        args = ' '.join( str( arg ) for arg in args )
        return fn( args )

    # Fix newfn's name and docstring
    setattr( newfn, '__name__', fn.__name__ )
    setattr( newfn, '__doc__', fn.__doc__ )
    return newfn

# Initialize logger and logging functions
logging.setLoggerClass(SysLogger)
lg = logging.getLogger("system")
_loggers = lg.info, lg.warning, lg.error, lg.debug
_loggers = tuple(makeListCompatible(logger) for logger in _loggers)
lg.info, lg.warning, lg.error, lg.debug = _loggers
info, warning, error, debug = _loggers
warn = warning  # alternate/old name
setLogLevel = lg.setLogLevel