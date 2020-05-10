import sys
import traceback

from azure.storage import CloudStorageAccount
from azure.storage.table import TableService, Entity

class TableOperate():
    """
    テーブル操作
    """
    def __init__(self,account=None):
        self.account = account
    def list_tables(self,account):
        try:
            table_service = account.create_table_service()
            tablelist = table_service.list_tables()
            return tablelist
        except Exception as e:
            print('Error Get list tables')
            t, v, tb = sys.exc_info()
            print(traceback.format_exception(t,v,tb))
            print(traceback.format_tb(e.__traceback__))
            return False
    def create_table(self,account,table_name):
        try:
            table_service = account.create_table_service()
            table_service.create_table(table_name)
            return True
        except Exception as e:
            print('Error creating table, ' + table_name + 'check if it already exists')
            t, v, tb = sys.exc_info()
            print(traceback.format_exception(t,v,tb))
            print(traceback.format_tb(e.__traceback__))
            return False
    def delete_table(self,account,table_name):
        try:
            table_service = account.create_table_service()
            if(table_service.exists(table_name)):
                table_service.delete_table(table_name)
                return True
        except Exception as e:
            print('Error Delete table, ' + table_name )
            t, v, tb = sys.exc_info()
            print(traceback.format_exception(t,v,tb))
            print(traceback.format_tb(e.__traceback__))
            return False

class RecordOperate():
    """
    レコード操作
    """
    def __init__(self,account=None,table_name=None):
        self.account = account
        self.tablename = table_name
    def insert_records(self,account,tablename,contents):
        try:
            table_service = account.create_table_service()
            if len(contents) == 1:
                r = contents[0]
                table_service.insert_or_replace_entity(tablename,r)
            elif len(contents) > 1 :  
                for r in contents:
                    table_service.insert_or_replace_entity(tablename,r)
            else:
                return False
            return True
        except Exception as e:
            print('Error Insert Record' )
            t, v, tb = sys.exc_info()
            print(traceback.format_exception(t,v,tb))
            print(traceback.format_tb(e.__traceback__))
            return False
    def getvalue_table(self,account,tablename,conditions):
        try:
            table_service = account.create_table_service()
            if type(conditions) is str:
               entity = table_service.query_entities(tablename, filter= conditions)
            elif type(conditions) is list and len(conditions) == 2:
               pk = conditions[0]
               rk = conditions[1]
               entity = table_service.get_entity(tablename, pk, rk)
            else :
               entity = table_service.get_entity(tablename)
            return entity
        except Exception as e:
            print('Error Get Records')
            t, v, tb = sys.exc_info()
            print(traceback.format_exception(t,v,tb))
            print(traceback.format_tb(e.__traceback__))
            return False
    def delete_records(self,account,tablename,conditions):
        try:
            table_service = account.create_table_service()
            if type(conditions) is str:
               se = table_service.query_entities(tablename, filter= conditions)
               for s in se:
                   pk = s.PartitionKey
                   rk = s.RowKey
                   entity = table_service.delete_entity(tablename, pk, rk)
            elif type(conditions) is list and len(conditions) == 2:
               pk = conditions[0]
               rk = conditions[1]
               entity = table_service.delete_entity(tablename, pk, rk)
            else :
               entity = table_service.delete_entity(tablename)
            return True
        except Exception as e:
            print('Error Get Records')
            t, v, tb = sys.exc_info()
            print(traceback.format_exception(t,v,tb))
            print(traceback.format_tb(e.__traceback__))
            return False