#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'JosePh.XRays'

import os
import sys
import threading


class ProxyThreading(threading.Thread):
    '''
    The thread class could get the result from the thread callback function ...
    '''

    def __init__(self, targetfunc=None, *args):
        threading.Thread.__init__(self, target=targetfunc, args=(args,))
        self.target = targetfunc
        self.args = args
        self.__result = None
        pass

    def run(self):
        self.__result = self.target(*self.args)
        pass

    def get_result(self):
        return self.__result
