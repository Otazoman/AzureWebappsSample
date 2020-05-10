
import json
import os
import sys
import traceback

import azure.common
from azure.storage import CloudStorageAccount

import config
from table_crud import TableOperate , RecordOperate
from tablestorage_account import TableStorageAccount

account_connection_string = config.STORAGE_CONNECTION_STRING

def main():
    try:
        # Authentication
        config = dict(s.split('=', 1) for s in account_connection_string.split(';') if s)
        account_name = config.get('AccountName')
        endpoint_suffix = config.get('EndpointSuffix')
        if endpoint_suffix == None:
            table_endpoint  = config.get('TableEndpoint')
            table_prefix = '.table.'
            start_index = table_endpoint.find(table_prefix)
            end_index = table_endpoint.endswith(':') and len(table_endpoint) or table_endpoint.rfind(':')
            endpoint_suffix = table_endpoint[start_index+len(table_prefix):end_index]
        account = TableStorageAccount(account_name = account_name, \
                                        connection_string = account_connection_string, \
                                        endpoint_suffix=endpoint_suffix)
    #Basic Table samples
        print ('---------------------------------------------------------------')
        print('Azure Storage Table samples')


        #tablename = 'testsample'
        to = TableOperate()
        ## テーブル一覧を取得する。
        tc0 = to.list_table(account)
        for l in tc0:
            print(l.name)
        ## テーブル作成
        #tc1 = to.create_table(account,tablename)
        #print(tc1)
        ## テーブル削除
        #tc2 = to.delete_table(account,tablename)
        #print(tc2)

        ro = RecordOperate()

        ### レコード追加
        """
        contents = [
            {'PartitionKey': '003', 'RowKey': '1', 'Value' : 'A'},
            {'PartitionKey': '004', 'RowKey': '2', 'Value' : 'B'},
            {'PartitionKey': '005', 'RowKey': '3', 'Value' : 'C'},
            {'PartitionKey': '006', 'RowKey': '4', 'Value' : 'D'},
            {'PartitionKey': '007', 'RowKey': '5', 'Value' : 'E'},
            {'PartitionKey': '008', 'RowKey': '6', 'Value' : 'F'},
            {'PartitionKey': '009', 'RowKey': '7', 'Value' : 'G'},
            {'PartitionKey': '010', 'RowKey': '8', 'Value' : 'H'},
            {'PartitionKey': '011', 'RowKey': '9', 'Value' : 'I'},
            {'PartitionKey': '012', 'RowKey': '10', 'Value' : 'J'}
        ]
        """
        #contents = [
        #    {'PartitionKey': '003', 'RowKey': '1', 'Value' : '0'}
        #]
        
        #tc3 = ro.insert_records(account=account,tablename=tablename,contents=contents)
        #print(tc3)

        ### レコード照会
        #conditions = ['003','1']
        #conditions = "PartitionKey eq '001'"
        #conditions = ""
        #tc4 = ro.getvalue_table(account=account,tablename=tablename,conditions=conditions)
        #if type(tc4) is azure.storage.table.models.Entity:
        #   print(type(tc4))
        #   print(tc4)
        #else:  
        #   print(type(tc4))
        #   for tc in tc4:
        #       print(tc.PartitionKey + " " + tc.RowKey + " " + tc.Value)

        ### レコード削除
        #conditions = ['003','1']
        #conditions = "PartitionKey eq '001'"
        #conditions = ""
        #tc5 = ro.delete_records(account=account,tablename=tablename,conditions=conditions)
        #print(tc5)

    except Exception as e:
        t, v, tb = sys.exc_info()
        print(traceback.format_exception(t,v,tb))
        print(traceback.format_tb(e.__traceback__))

if __name__ == '__main__':
   main()
