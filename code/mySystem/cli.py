"CLI module"

__author__ = 'fan'

import os
from cmd import Cmd
from func import load_sysConfig, play_game
from log import lg, LEVELS, info, debug, warn, error

class CLI(Cmd):
    prompt = 'testSys> '
    intro = ('\n          ****************************\n'
            '            Welcom to my test system\n'
            '          ****************************\n')

    def __init__(self):
        Cmd.__init__(self)
        self.run()

    def run(self):
        while True:
            try:
                self.cmdloop()
                break
            except KeyboardInterrupt:
                # Output a message - unless it's also interrupted
                # pylint: disable=broad-except
                try:
                    warn('CLI run() Interrupt')
                except Exception:
                    pass
                # pylint: enable=broad-except
    
    def emptyline(self):
        "Don't repeat last command when you hit return."
        pass

    helpInfo = ('You may also send a command to a node using:\n'
                '  <node> command {args}\n')

    def do_help(self, _line):
        "show help info"
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
        "show current file in current dir"
        curDirFiles = [x for x in os.listdir('.') if os.path.isdir(x)]
        print("My file list:")
        for file in curDirFiles:
            print(file)
    
    def do_load_config(self, _line):
        load_sysConfig(_line)
    
    def do_play_game(self, _line):
        play_game()
    
    def do_exit(self, _line):
        "exit system"
        print('bye!')
        return 'exited by user command'