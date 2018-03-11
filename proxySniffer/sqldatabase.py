#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'JosePh.XRays'

import os
import sys
import sqlite3
import pymysql

class sqlBaseOption(object):
    def __init__(self):
        self.table_filed_5= ['ID', 'Host_IP_Address', 'Host_Port', 'Anonymity', '_Type', 'Location']
        self.table_filed_10= ['ID', 'Host_IP_Address', 'Host_Port','_Type', 'Anonymity', 'Location','Speed','ConnTime','AliveTime','AuthTime']
    def connect(self):
        pass
    def export(self):
        pass

class ProxySqlite3(sqlBaseOption):
    def __init__(self,db_path=None,lsdata=None,overwrite=True):
        '''
        Export proxy list to sqlite3 database file
        :param db_path: => sqlite3 db path
        :param lsdata: => proxy.toList()
        :param overwrite: => is overwrite the old db file
        '''
        super().__init__()
        self.db_path=db_path
        self.lsdata=lsdata
        self.overwrite=overwrite
        self.connect()


    def connect(self):
        if not self.db_path:
            return
        if os.path.exists(self.db_path):
            if self.overwrite:
                os.unlink(self.db_path)
                pass
        self.conn= sqlite3.connect(self.db_path)
        self.cursor=self.conn.cursor()

    def export(self):

        if self.lsdata is None:
            self.cursor.close()
            self.conn.close()
            return False

        print('Exporting...')
        length_rows = len(self.lsdata)
        length_column = len(self.lsdata[0])

        create_tb_query=''
        if length_column==5:
            create_tb_query='create table tb_proxies(' \
            '{0} int primary key not null,' \
            '{1} char(20),' \
            '{2} int,' \
            '{3} char(10),' \
            '{4} char(10),' \
            '{5} char(30) );'.format(self.table_filed_5[0],
                                     self.table_filed_5[1],
                                     self.table_filed_5[2],
                                     self.table_filed_5[3],
                                     self.table_filed_5[4],
                                     self.table_filed_5[5])
        else:

            create_tb_query='create table tb_proxies(' \
            '{0} int primary key not null,' \
            '{1} char(20),' \
            '{2} int,' \
            '{3} char(15),' \
            '{4} char(15),' \
            '{5} char(10),' \
            '{6} char(10),' \
            '{7} char(10),' \
            '{8} char(10),' \
            '{9} char(20) );' .format(self.table_filed_10[0],
                        self.table_filed_10[1],
                        self.table_filed_10[2],
                        self.table_filed_10[3],
                        self.table_filed_10[4],
                        self.table_filed_10[5],
                        self.table_filed_10[6],
                        self.table_filed_10[7],
                        self.table_filed_10[8],
                        self.table_filed_10[9]
                    )

        self.cursor.execute(create_tb_query)
        self.conn.commit()

        index=0
        for row in self.lsdata:
            index+=1

            if length_column==5:
                line = 'insert into tb_proxies (ID,Host_IP_Address,Host_Port,Anonymity,_Type,Location)' \
                      " values ({0},'{1}',{2},'{3}','{4}','{5}') ;"\
                    .format(index, row[0], row[1], row[2],row[3],row[4])
            else:
                line = 'insert into tb_proxies (ID,Host_IP_Address,Host_Port,_Type,Anonymity,Location,Speed,ConnTime,AliveTime,AuthTime)' \
                      " values ({0},'{1}',{2},'{3}','{4}','{5}','{6}','{7}','{8}','{9}') ;"\
                    .format(index, row[0], row[1], row[2],row[3],row[4],
                            row[5], row[6], row[7], row[8])

            self.cursor.execute(line)
            self.conn.commit()

        self.cursor.close()
        self.conn.close()
        print('Exported completely!')
        return True
        pass