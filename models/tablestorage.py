import json
import os
import re
import sys
import traceback

import azure.common
from azure.storage import CloudStorageAccount

import config
from table_crud import TableOperate , RecordOperate
from tablestorage_account import TableStorageAccount

class TableStorageOperate:
    """ Table Storage Operate Class """
    def __init__(self):
        # connectionstring
        account_connection_string = config.STORAGE_CONNECTION_STRING
        auth = dict(s.split('=', 1) for s in account_connection_string.split(';') if s)
        account_name = auth.get('AccountName')
        endpoint_suffix = auth.get('EndpointSuffix')
        if endpoint_suffix == None:
            table_endpoint  = auth.get('TableEndpoint')
            table_prefix = '.table.'
            start_index = table_endpoint.find(table_prefix)
            end_index = table_endpoint.endswith(':') and len(table_endpoint) or table_endpoint.rfind(':')
            endpoint_suffix = table_endpoint[start_index+len(table_prefix):end_index]
        # Authentication
        self.account = TableStorageAccount(account_name = account_name, \
                                        connection_string = account_connection_string, \
                                        endpoint_suffix = endpoint_suffix)       
    def insert_table(self,file,tablename):
        """ Create Table and Upsert Table"""
        try:
            contents = []
            to = TableOperate()
            to.create_table(account=self.account,table_name=tablename)
            if to:
                #ファイル読込
                with open(file, "r") as test_data:
                    for l in test_data:
                        if re.search('{*}',l):
                            s = l.strip().rstrip(",")
                            contents.append(json.loads(s))
                ro = RecordOperate()
                ir = ro.insert_records(account=self.account,tablename=tablename,contents=contents)
                return ir
        except Exception as e:
            t, v, tb = sys.exc_info()
            print(traceback.format_exception(t,v,tb))
            print(traceback.format_tb(e.__traceback__))
            return False
    def select_records(self,condition,tablename):
        """ Set Condition and Select"""
        try:
            ro = RecordOperate()
            sr = ro.getvalue_table(account=self.account,tablename=tablename,conditions=condition)
            return sr
        except Exception as e:
            t, v, tb = sys.exc_info()
            print(traceback.format_exception(t,v,tb))
            print(traceback.format_tb(e.__traceback__))
            return False
    def delete_records(self,condition,tablename):
        """ Set Condition and Delete"""
        try:
            ro = RecordOperate()
            dr = ro.delete_records(account=self.account,tablename=tablename,conditions=condition)
            return dr
        except Exception as e:
            t, v, tb = sys.exc_info()
            print(traceback.format_exception(t,v,tb))
            print(traceback.format_tb(e.__traceback__))
            return False
    def get_table_list(self):
        """ All Tables """
        try:
            to = TableOperate()
            tl = to.list_tables(account=self.account)
            tables = [ l.name for l in tl ]
            return tables
        except Exception as e:
            t, v, tb = sys.exc_info()
            print(traceback.format_exception(t,v,tb))
            print(traceback.format_tb(e.__traceback__))
            return False
    def get_default_table(self,listtables):
        """ Avail Record Table """
        try:
            conditions=""
            ro = RecordOperate()
            for lt in listtables:
                tc0 = ro.getvalue_table(account=self.account,tablename=lt,conditions=conditions)
                tablenames = [ r for r in tc0 if r ]
            return tablenames
        except Exception as e:
            t, v, tb = sys.exc_info()
            print(traceback.format_exception(t,v,tb))
            print(traceback.format_tb(e.__traceback__))
            return False
