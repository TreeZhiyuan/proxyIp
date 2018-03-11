#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'JosePh.XRays'

import os
import sys
import re
import requests
import threading
import subprocess
import datetime
from termcolor import colored

from proxyThread import ProxyThreading

# 国内高匿代理
INTERNAL_HIGHANONYMITY_PROXY=0
# 国内普通代理
INTERNAL_COMMON_PROXY=1
# 国内HTTP代理
INTERNAL_HTTP_PROXY=4
# 国内HTTPS代理
INTERNAL_HTTPS_PROXY=5

# 国外高匿代理
EXTERNAL_HIGHANONYMITY_PROXY=2
# 国外普通代理
EXTERNAL_COMMON_PROXY=3


class Proxies(object):
    '''
    This is a base class,but I not recommend you to use it
    '''
    def __init__(self,url,
                 headers=None,
                 pattern=None,
                 pattern_header=None,
                 proxies=None,
                 timeout=5,
                 typeproxy=None,
                 chardet='utf-8'):

        if headers==None:
            self.headers=headers = {
             'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36'
            }
        else:
            self.headers = headers

        self.url=url
        self.proxies=proxies
        self.timeout=timeout
        self.result=[]
        self.typeproxy=typeproxy
        self.chardet=chardet

        self.pattern=pattern
        self.pattern_header=pattern_header
        pass

    def getDateTimeNow(self):
        return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def pack_urlquery(self, index):
        '''
        Must be overrided,to parse the url string
        :param index: page number
        :return: return a new url string and open it in _getSources
        '''
        pass

    def _getSources(self,numberpage=1):
        '''
        Get url source text,must be overrided
        :param numberpage: the INDEX of page
        :return:
        '''
        if self.headers is None:
            return
        try:
            self.url= self.pack_urlquery(numberpage)
            print(colored('get=> '+self.url,'green',None,['underline']))
            with requests.Session() as sess:
                if self.proxies is not None:
                    sess.proxies = self.proxies
                req= requests.Request(method='GET',url=self.url,headers=self.headers)
                preq= sess.prepare_request(req)
                send_kwargs = {
                    'timeout': self.timeout
                }
                resp= sess.send(preq,**send_kwargs)

                # try to convert gbk to utf-8
                if self.chardet.lower()=='gbk' or self.chardet.lower()=='gb2312':
                    text = resp.content.decode('gbk').encode('utf-8').decode('utf-8')
                else:
                    text = resp.text
                return text
        except IOError as e:
            print(e.args)
            return None
        pass

    def _getIPs(self,maxPage=2):
        '''
        May be overrided
        :param maxPage: maximum of the pages
        :return:
        '''
        if maxPage<=0:
            return None

        ls_source=[]

        for i in range(maxPage):
            tmpTh = ProxyThreading(self._threadfunc, i+1)
            tmpTh.start()
            tmpTh.join()
            source = tmpTh.get_result()
            ls_source.append(source)
        for perpage in ls_source:
            _ips = []
            _ports=[]
            _anonymity=[]
            _type=[]
            _location=[]

            rex = re.compile(self.pattern, re.IGNORECASE)
            lsall= rex.findall(perpage)
            if lsall is not None :

                for per in lsall:
                    if(per[0]==self.pattern_header[0]):_ips.append(per[1])
                    if(per[0]==self.pattern_header[1]):_ports.append(per[1])
                    if(per[0]==self.pattern_header[2]):_anonymity.append(per[1])
                    if(per[0]==self.pattern_header[3]):_type.append(per[1])
                    if(per[0]==self.pattern_header[4]):_location.append(per[1])
            else:
                return  None

            if _ips is not  None:
                for i in range(len(_ips)):
                    _lineinfo = {
                        'ip': _ips[i],
                        'port': _ports[i],
                        'anonymity': _anonymity[i],
                        'type': _type[i],
                        'location': _location[i],
                    }
                    self.result.append(_lineinfo)
                    pass
            else:
                return None

    def Go(self, maxPage=2):
        '''
        May be overrided,call the _getIPs
        :param maxPage:
        :return:
        '''
        self._getIPs(maxPage)
        pass

    def _threadfunc(self,*args):
        '''
        Thread callback
        class: => ProxyThreading
        :param args:
        :return: the source code of the url
        '''
        source = self._getSources(numberpage=args[0])
        return source

    def _encode_(self,string):
        if type(string)==str:
            return string.encode('utf-8')
    def saveFile(self,file,overwrite=False,reporter_used=False):
        '''
        Save result to a file
        :param file:    file-obj or filename
        :param overwrite:   is overwrite?
        :param reporter:    set a reporter mode,it can be used by ProxyChecker class
        :return: True|False
        '''
        if self.result is None:
            return False
        if file==None:
            return False
        if not hasattr(file,'write'):
            if os.path.exists(file):
                print(colored(('=> [ %s ] existed!' % file),'yellow'))
                if (overwrite==False):
                    return False
            file=open(file,'wb+')

        # enable the reporter mode
        if reporter_used==True:

            for i in self.toDict():
                host,port=i.get('ip'),i.get('port')
                file.write(self._encode_(host+':'+port+'\n'))
            file.close()
            return True
        file.write(self._encode_('Write time: '+self.getDateTimeNow()+"\n\n"))

        if len(dict(self.result[0]).keys()) == 5:
            headers = ['ID', 'Host_IP_Address', 'Host_Port', 'Anonymity', 'Type', 'Location']
        else:
            headers = ['ID', 'Host_IP_Address', 'Host_Port','Type', 'Anonymity', 'Location','Speed','ConnTime','AliveTime','AuthTime']

        for p in headers:
            file.write(self._encode_(p+'\t'))
        file.write(self._encode_('\n'))

        index=0
        lsrows=self.toDict()
        for i in lsrows:
            index+=1
            file.write(self._encode_(str(index) + '\t'))
            for value in i.values():
                file.write(self._encode_(value+'\t'))
            file.write(self._encode_('\n'))
        file.close()
        return True


    '''
        [
            {'ip':'127.0.0.1','port':'8888','anonymity':'xxx','type':'http','location':'china'}
            {'ip':'127.0.0.1','port':'8888','anonymity':'xxx','type':'http','location':'china'}
            {'ip':'127.0.0.1','port':'8888','anonymity':'xxx','type':'http','location':'china'}
            ......            
        ]
        
        =>
        
        [
            ['127.0.0.1','8888','xxxx','http','china'],
            ['127.0.0.1','8888','xxxx','http','china'],
            ['127.0.0.1','8888','xxxx','http','china']
            ......
        ]
        
    '''
    def toList(self):
        if self.result is not None:
            ls_rows=[]
            for i in self.result:
                l = []
                for k,v in i.items():
                    l.append(v)
                ls_rows.append(l)
            if ls_rows:
                return ls_rows
            else:
                return None
        else:
            return None
    def toDict(self):
        if self.result is not None:
            return self.result
        else:
            return None

class KuaiProxy(Proxies):

    def __init__(self,
                 pattern=None,
                 pattern_header=None,
                 url=None,
                 headers=None,
                 proxies=None,
                 timeout=5,
                 typeproxy=INTERNAL_COMMON_PROXY,
                 chardet='utf-8'):
        '''
        :param pattern:
        :param pattern_header:
        :param url:
        :param headers:
        :param proxies:
        :param timeout:
        :param typeproxy: only support INTERNAL_HIGHANONYMITY_PROXY | INTERNAL_COMMON_PROXY

        '''

        if pattern == None:
            self.pattern = '<td data-title="(.*?)">(.*?)</td>'
        else:
            self.pattern = pattern

        if pattern_header == None:
            self.pattern_header = ['IP', 'PORT', '匿名度', '类型', '位置']
        else:
            self.pattern_header = pattern_header

        super().__init__(
            pattern=self.pattern,
            pattern_header=self.pattern_header,
            url=url,
            headers=headers,
            proxies=proxies,
            typeproxy=typeproxy,
            timeout=timeout,
            chardet=chardet
        )

        self.typeproxy=INTERNAL_COMMON_PROXY

        self.server='https://www.kuaidaili.com/free'
        if url==None:
            self.url = self.server
        else:
            self.url=url

        if headers !=None:
            self.headers = headers

    def pack_urlquery(self,index):
        '''
           example:  https://www.kuaidaili.com/free/inha/1
        :param index:
        :return:
        '''
        str_tmp=''
        if self.typeproxy==INTERNAL_COMMON_PROXY:
            str_tmp = 'intr'
        else:
            str_tmp = 'inha'
        return self.server+'/'+str_tmp+'/'+str(index)

class YaoyaoProxy(Proxies):

    def __init__(self,
                 pattern=None,
                 pattern_header=None,
                 url=None,
                 headers=None,
                 proxies=None,
                 timeout=5,
                 typeproxy=INTERNAL_COMMON_PROXY,
                 chardet='gb2312'):
        '''

        :param pattern:
        :param pattern_header:
        :param url:
        :param headers:
        :param proxies:
        :param timeout:
        :param typeproxy:
        :param chardet:
        '''
        if pattern==None:
            self.pattern='<td class="(.*?)">(.*?)</td>'
        else:
            self.pattern=pattern
        if pattern_header==None:
            self.pattern_header=['style1','style2','style3','style4','style5']
        else:
            self.pattern_header=pattern_header

        super().__init__(
            pattern=self.pattern,
            pattern_header=self.pattern_header,
            url=url,
            headers=headers,
            proxies=proxies,
            typeproxy=typeproxy,
            timeout=timeout,
            chardet=chardet
        )
        self.typeproxy=typeproxy
        self.server='http://www.httpsdaili.com/free.asp'
        if url==None:
            self.url = self.server
        else:
            self.url=url

        if headers !=None:
            self.headers = headers


    def pack_urlquery(self, index):
        '''
        Return the new url by construct
            example: http://www.httpsdaili.com/free.asp?stype=2&page=1
        :param index:
        :return:
        '''

        str_url_tmp=''
        if self.typeproxy==INTERNAL_HIGHANONYMITY_PROXY:
            str_url_tmp='stype=1'
        elif self.typeproxy==INTERNAL_COMMON_PROXY:
            str_url_tmp='stype=2'
        elif self.typeproxy==EXTERNAL_HIGHANONYMITY_PROXY:
            str_url_tmp='stype=3'
        else:
            str_url_tmp='stype=4'

        return self.server+'?'+str_url_tmp+'&'+'page'+str(index)

class XiciProxy(Proxies):

    def __init__(self,
                 pattern=None,
                 pattern_header=None,
                 url=None,
                 headers=None,
                 proxies=None,
                 timeout=5,
                 typeproxy=INTERNAL_COMMON_PROXY,
                 chardet='utf-8'):
        '''

        :param pattern:
        :param pattern_header:
        :param url:
        :param headers:
        :param proxies:
        :param timeout:
        :param typeproxy:
        :param chardet:
        '''
        super().__init__(pattern=pattern,
                         pattern_header=pattern_header,
                         url=url,
                         headers=headers,
                         proxies=proxies,
                         timeout=timeout,
                         typeproxy=typeproxy,
                         chardet=chardet)
        self.server='http://www.xicidaili.com'
        if(url==None):
            self.url = self.server
        else:
            self.url=url

        if headers !=None:
            self.headers = headers
        self.pattern='<td>(.*?)</td>\s+'\
            '<td>(.*?)</td>\s+'\
            '<td>\s+'\
            '<a href="(.*?)">(.*?)</a>\s+'\
            '</td>\s+'\
            '<td class="country">(.*?)</td>\s+'\
            '<td>(.*?)</td>\s+'\
            '<td class="country">\s+'\
            '<div title="(.*?)" class="bar">\s+'\
            '<div class="bar_inner (.*?)" style="width:(.*?)">\s+'\
            '</div>\s+'\
            '</div>\s+'\
            '</td>\s+'\
            '<td class="country">\s+'\
            '<div title="(.*?)" class="bar">\s+'\
            '<div class="bar_inner (.*?)" style="width:(.*?)">\s+'\
            '</div>\s+'\
            '</div>\s+'\
            '</td>\s+'\
            '<td>(.*?)</td>\s+'\
            '<td>(.*?)</td>\s+'\
            '</tr>\s+'

    def pack_urlquery(self, index):
        # http://www.xicidaili.com/nt/2

        str_tmp=''
        if self.typeproxy==INTERNAL_COMMON_PROXY:
            str_tmp='nt'
        if self.typeproxy==INTERNAL_HIGHANONYMITY_PROXY:
            str_tmp='nn'
        if self.typeproxy==INTERNAL_HTTP_PROXY:
            str_tmp='wt'
        if self.typeproxy==INTERNAL_HTTPS_PROXY:
            str_tmp='wn'
        return self.server+'/'+str_tmp+'/'+str(index)

    def _getIPs(self,maxPage=2):

        if maxPage<=0:
            return None

        ls_sources=[]
        for index in range(maxPage):
            th= ProxyThreading(self._threadfunc, index+1)
            th.start()
            th.join()
            ls_sources.append(th.get_result())

        if len(ls_sources)==0:
            return None
        for source in ls_sources:
            rx = re.compile(self.pattern, re.IGNORECASE)
            if rx==None:
                break
            _ips = []
            _ports = []
            _type = []
            _anonymity = []
            _location = []
            _speed = []
            _connect_time = []
            _alive_time = []
            _auth_time = []
            
            try:
                ls = rx.findall(source)
            except Exception as e:
                print(e)
                break

            for l in ls:
                # iteator
                li = iter(l)
                while True:
                    try:
                        _ips.append(next(li))
                        _ports.append(next(li))
                        next(li)
                        _location.append(next(li))
                        _anonymity.append(next(li))
                        _type.append(next(li))
                        next(li)
                        next(li)
                        _speed.append(next(li))
                        next(li)
                        next(li)
                        _connect_time.append(next(li))
                        _alive_time.append(next(li))
                        _auth_time.append(next(li))

                    except StopIteration as e:
                        break

            for i in range(len(_ips)):
                line = {
                    'ip': _ips[i],
                    'port': _ports[i],
                    'type': _type[i],
                    'anonymity': _anonymity[i],
                    'location': _location[i],
                    'speed': _speed[i],
                    'connect_time': _connect_time[i],
                    'alive_time': _alive_time[i],
                    'auth_time': _auth_time[i],
                }
                self.result.append(line)
