#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"CLI module"

__author__ = 'fan'

from cmd import Cmd
from lib.func import load_sysConfig
import os

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

    def do_help(self, _line):
        "显示可以使用的命令"
        Cmd.do_help(self, _line)
        if _line == '':
            print(self.helpInfo)
    
    def do_readfile(self, _line):
        if _line is '':
            print('Please enter file name.')
        else:
            with open(_line, 'r', encoding='utf-8') as f:
                print(f.read())
    
    def do_ls(self, _line):
        "显示当前目录下所有文件"
        curDirFiles = [x for x in os.listdir('.') if os.path.isdir(x)]
        print("My file list:")
        for file in curDirFiles:
            print(file)
    
    def do_load_config(self, _line):
        load_sysConfig(_line)
    
    def do_exit(self, _line):
        "退出"
        print('exit...')
        return 'exited by user command'