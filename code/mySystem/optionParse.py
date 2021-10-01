#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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

if __name__ == "__main__":
    Run()