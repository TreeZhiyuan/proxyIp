#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'JosePh.XRays'
__DateTime__='2018-03-11 12:18:26'


import os
import sys
import texttable
import re
from optparse import OptionParser,OptionGroup
from termcolor import colored

import ProxyBase
from ProxyBase import KuaiProxy,YaoyaoProxy,XiciProxy
from proxyChecker import ProxyChecker
from SignPic import SignLogo
from sqldatabase import ProxySqlite3

def website_proxy():

    print('Proxy Websites:')
    print('+=========================================+')
    print('| => 1.西刺代理: ' + colored('http://www.xicidaili.com', 'yellow') + ' |')
    print('| => 2.瑶瑶代理: ' + colored('https://www.kuaidaili.com', 'yellow') + '|')
    print('| => 3.快代理: ' + colored('http://www.httpsdaili.com', 'yellow') + '  |')
    print('+=========================================+')


def select_typeProxy(type):
    if type==1:
        proxy = XiciProxy(typeproxy=ProxyBase.INTERNAL_HTTP_PROXY)
    elif type==2:
        proxy = YaoyaoProxy(typeproxy=ProxyBase.INTERNAL_COMMON_PROXY)
    else:
        proxy = KuaiProxy(typeproxy=ProxyBase.INTERNAL_COMMON_PROXY)
    return proxy


def drawTable(_type,ls):
    if type(ls)!=list:
        return
    table = texttable.Texttable(len(ls))
    if _type==1:
        table.set_cols_width([15, 5, 5, 5, 10, 4, 4, 5, 20])
        table.header(['Ip', 'Port', 'Type', 'Anonymity', 'Location', 'Speed', 'Connt', 'Alivet', 'Autht'])
    else:
        table.set_cols_width([15,5,10,5,20])
        table.header(['Ip', 'Port', 'Anonymity', 'Type', 'Location'])

    table.set_deco(texttable.Texttable.BORDER|
                   texttable.Texttable.VLINES|
                   texttable.Texttable.HEADER)

    table.add_rows(ls,False)
    return table.draw()

def mainFunction():
    SignLogo().proxySnifferLogo()

    optParser = OptionParser(version='1.0.0')
    optParser.set_usage('proxySniffer.py [-s [-o OFILE]] [-c -f FILE -o OFILE] [-u]')
    optParser.add_option('--author', dest='author', action='store_true', help='show the author info')
    optParser.add_option('-u', dest='urls', action='store_true', help='show the support proxy ip website')
    optParser.add_option('-r','--reconnect',metavar='MAXNUM',type='int',dest='reconnect',action='store',help='test the proxy ip reconnect maximumn')
    optParser.add_option('-c', '--check', dest='check', action='store_true',help='check the reporter proxies was available')
    optParser.add_option('-f', '--filename', type='string', metavar='FILE', dest='filename', action='store',help='specify a host proxy file')
    optParser.add_option('-o', '--output', metavar='OFILE', dest='output', action='store',help='output the file to disk,defalut:[stdout]')
    optParser.add_option('-s', '--search', dest='search', action='store_true', help='search the free proxy on website')

    optgGroup=OptionGroup(optParser,'Export SQL Database','You can export the proxy info to database')
    optgGroup.add_option('--sqlite3',metavar='PATH',dest='sqlite3',help='Export proxy to sqlite3 database')
    optParser.add_option_group(optgGroup)

    (opts,args) = optParser.parse_args()

    if opts.author:
        print('Author: JosePh.XRays')
        print('Blog: http://josephxy.com')
        print('Email: josephxrays@gmail.com')
        print('Thanks !')
        exit(0)

    if (opts.urls == True):
        website_proxy()
        exit(0)

    if (opts.check == True):

        if opts.reconnect !=None and opts.reconnect!='':
            reconnectmax=eval(str(opts.reconnect))
            if reconnectmax < 0 and reconnectmax >100:
                print('=> To large reconnect maximum!')
                exit(0)
        else:
            reconnectmax=5

        if opts.filename is not None:
            if (os.path.exists(opts.filename)):
                with open(opts.filename, 'r+') as f:
                    print(colored('=> Start check the proxy file... wait a moment...', 'green'))
                    checker = ProxyChecker(f)
                    if opts.output == None:
                        checker.check(reconnection=reconnectmax)
                    else:
                        checker.check(outputfile=opts.output,reconnection=reconnectmax)
                    print(colored('=> Check the proxy file completely!', 'green'))
                    exit(0)

    if (opts.search == True):
        website_proxy()

        typeproxy = input('proxy class[1]=> ').strip()
        if typeproxy == '':
            print('=> [西刺代理]')
            typeproxy = 1
        elif typeproxy == '1':
            print('=> [西刺代理]')
            typeproxy = 1
        elif typeproxy == '2':
            print('=> [瑶瑶代理]')
            typeproxy = 2
        elif typeproxy == '3':
            print('=> [快代理]')
            typeproxy = 3
        else:
            print('=> ERROR!')
            exit(-1)

        maximum = input('maximum pages[2]=> ').strip()
        if maximum == '':
            maximum = 2
        elif maximum.isnumeric():
            maximum = eval(maximum)

        print('=>0: 国内高匿代理')
        print('=>1: 国内普通代理')
        print('=>2: 国外高匿代理')
        print('=>3: 国外普通代理')
        print('=>4: 国内HTTP代理')
        print('=>5: 国内HTTPS代理')

        proxymethod = input('proxymethod [1]=> ').strip()
        if proxymethod == '':
            proxymethod = 1

        elif proxymethod.isnumeric():
            proxymethod = eval(proxymethod)

        isreporter = input('reporter mode[no]=> ').strip()
        if isreporter.lower() == 'no':
            isreporter = False
        elif isreporter.lower()=='yes':
            isreporter = True

        print(colored('Start search proxy list...', 'green', None, ['bold']))
        proxy = select_typeProxy(typeproxy)
        proxy.Go(maxPage=maximum)
        lst = proxy.toList()

        # output proxy ip list
        print(drawTable(typeproxy, lst))

        # export the file
        if not opts.output:
            opts.output = input('save file path => ').strip()
            if opts.output == '':
                opts.output = None
                pass
        if opts.output:
            if (proxy.saveFile(opts.output, True, bool(isreporter))):
                print('Save file successfully!')
            else:
                print('Save file failed!')

        # export to sqlite3
        if opts.sqlite3:
            proxy_sqlite3 = ProxySqlite3(opts.sqlite3, lst)
            proxy_sqlite3.export()

        print(colored('Completely search proxy list...', 'green', None, ['bold']))
        print(colored('Have a nice time:)', 'yellow', None, ['bold', 'underline']))
        exit(0)

if __name__ == '__main__':

    '''
    Example: 
        ==> proxySniffer.py -c -f proxy.lst -r 10
        ==> proxySniffer.py -s -o output.txt
        ==> proxySniffer.py -s --sqlite3=test.db
    '''

    mainFunction()

    pass
