#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"CLI module"

__author__ = 'fan'

from cmd import Cmd

class CLI(Cmd):
    prompt = 'testSys> '
    intro = ('\n          ****************************\n'
            '            Welcom to my test system\n'
            '          ****************************\n')

    def __init__(self):
        Cmd.__init__(self)
        self.run()

    def run(self):
        self.cmdloop()
    
    def emptyline(self):
        "输入回车后不会重复上一次的命令"
        pass

    helpInfo = ('You may also send a command to a node using:\n'
                '  <node> command {args}\n')

    def do_help(self, line):
        "显示可以使用的命令"
        Cmd.do_help(self, line)
        if line == '':
            print(self.helpInfo)
    
    def do_readfile(self, _line):
        if _line is '':
            print('Please enter file name.')
        else:
            with open(_line, 'r', encoding='utf-8') as f:
                print(f.read())
    
    def do_exit(self, _line):
        "退出"
        print('exit...')
        return 'exited by user command'