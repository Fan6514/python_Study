#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import psutil
from optparse import OptionParser
from log import lg, LEVELS, info, debug, warn, error
from cli import CLI

class Run(object):
    "Run system"

    def __init__(self):
        "Init."
        self.options = None
        self.args = None

        self.parseArgs()
        self.setup()
        self.begin()

    def parseArgs(self):
        desc = ("This is a test for cmd args input.")
        usage = ('%prog [options]\n'
                 '(type %prog -h for details)')
        version = ("0.0.1")

        opts = OptionParser(description=desc, usage=usage, version=version)
        opts.add_option('-c', '--config', action='store',
                        default=False, help='write config to FILE')
        opts.add_option('-v', '--verbosity', type='choice',
                        choices=list(LEVELS.keys()), default = 'warn',
                        help='|'.join(LEVELS.keys()))
        
        self.options, self.args = opts.parse_args()

    def setup(self):
        "Set up logging verbosity"
        if self.options.verbosity not in LEVELS.keys():
            warn('selected verbosity level (%s) is not log level\n'
                'Please restart system with -v [debug, info, warn, error].\n'
                % self.options.verbosity)
        lg.setLogLevel(self.options.verbosity)
    
    def begin(self):
        "Create and run test system"
        global CLI, line

        CLI = CLI()

# 打印当前程序占用的内存大小
def print_memory_info(name):
    pid = os.getpid()
    p = psutil.Process(pid)

    info = p.memory_full_info()
    MB = 1024 * 1024
    memory = info.uss / MB
    print('%s used %d MB' % (name, memory))

if __name__ == "__main__":
    try:
        print_memory_info("System start")
        Run()
        print_memory_info("System end")
    except KeyboardInterrupt:
        info("\n\nKeyboard Interrupt. Shutting down system...\n\n")
    except Exception:
        type_, val_, trace_ = sys.exc_info()
        errorMsg = ( "-"*80 + "\n" +
                     "Caught exception. Cleaning up...\n\n" +
                     "%s: %s\n" % ( type_.__name__, val_ ) +
                     "-"*80 + "\n" )
        error( errorMsg )
        # Print stack trace to debug log
        import traceback
        stackTrace = traceback.format_exc()
        debug( stackTrace + "\n" )