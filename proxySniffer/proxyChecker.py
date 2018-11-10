#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'JosePh.XRays'

import socket
import os
import sys
import urllib
import requests
import re
import time
from termcolor import colored
import signal
import demjson

class ProxyChecker(object):

    def sighandler(self,signo,stack_frame):
        self.ischecking=False
        print(colored('Bye~','red',None,['bold']))
        self.file.close()
        pass

    def __init__(self,file,headers=None,timeout=2):
        if not hasattr(file,'read'):
            file= open(file=file,mode='r+')

        self.file=file

        if headers==None:
            self.headers=headers = {
             'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36'
            }
        else:
            self.headers = headers
        self.timeout=timeout
        self.ischecking=False

        socket.setdefaulttimeout(self.timeout)
        signal.signal(signal.SIGINT, self.sighandler)

    def check(self,outputfile=None,reconnection=5):
        self.ischecking=True
        index = 0

        if outputfile!=None:
            try:
                fileoutput = open(outputfile, 'wb+')
            except Exception as e:
                print(e)
                return
        else:
            fileoutput=None
        while True:
            if self.ischecking==False:
                break
            line = self.file.readline().strip()
            if line == None or line=="":
                break
            proxies = {'http': 'http://'+line.split(':')[0] + ':' + line.split(':')[1]}
            print("["+str(index)+"] Checking=> "+proxies.get('http'))

            index += 1
            # reconnect three times
            for i in range(reconnection):
                if self.ischecking==False:
                    break
                try:
                    resp = requests.session().request(method='GET',
                                                      url='http://ip.chinaz.com/getip.aspx',
                                                      headers=self.headers,
                                                      proxies=proxies, timeout=self.timeout)
                    if resp.status_code==200 :
                        try:
                            dc = demjson.decode(resp.text, encoding='utf-8')
                            print(colored('=>[GOOD]: ' + resp.url, 'green', None, ['bold']) )
                            print('\t==> '+dc.get('ip') + ':' + dc.get('address'))
                        except:
                            resp.close()
                            pass

                        if fileoutput:
                            fileoutput.write((proxies.get('http') + '\n').encode('utf-8'))
                            fileoutput.flush()
                        resp.close()
                        break
                    else:
                        print(colored('=>[BAD]: ' + resp.url, 'red', None, ['bold']))
                        resp.close()
                    time.sleep(0.2)
                except requests.RequestException as e:
                    #print(e.strerror)
                    break

        if fileoutput:
            fileoutput.close()
        self.file.close()
        pass
