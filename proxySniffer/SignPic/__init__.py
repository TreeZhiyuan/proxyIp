#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'JosePh.XRays'

import os
import sys
from termcolor import colored
import datetime


class SignLogo:
    def __init__(self):
        pass

    def proxySnifferLogo(self):
        print()
        print('========================================')
        print(colored('=======', 'yellow', None, ['bold']) + '             =    = ')
        print(colored('==', 'yellow', None, ['bold']) + '   ' + colored('==', 'yellow', None, ['bold']) + ' ' + colored(
            'proxySniffer', 'green', None, ['bold', 'underline']) + ' =  =   **   ** ')
        print(colored('==', 'yellow', None, ['bold']) + '   ' + colored('==', 'yellow', None,
                                                                        ['bold']) + '               $      ** **')
        print(colored('=======', 'yellow', None, ['bold']) + ' ===   +++     $       *** ')
        print(colored('==', 'yellow', None, ['bold']) + '      =  = +   +   = =      *** ')
        print(colored('==', 'yellow', None, ['bold']) + '      =    +   +  =   =     ***')
        print(colored('==', 'yellow', None, ['bold']) + '      =     +++  =     =    ***')
        print('===========' + colored(datetime.datetime.now().strftime('%Y:%m:%d %H:%M:%S'), 'red') + '==========')
        print()
