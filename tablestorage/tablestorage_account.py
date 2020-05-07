from azure.storage import SharedAccessSignature
from azure.storage.table import TableService, Entity

class TableStorageAccount(object):

    def __init__(self, account_name=None, connection_string=None, sas_token=None, endpoint_suffix = 'cosmosdb.windows.net', is_emulated=None):
        self.account_name = account_name
        self.connection_string = connection_string
        self.sas_token = sas_token
        self.endpoint_suffix = endpoint_suffix		
        self.is_emulated = is_emulated

    def create_table_service(self):
        return TableService(account_name = self.account_name,
                            sas_token=self.sas_token,
                            endpoint_suffix=self.endpoint_suffix, 
                            connection_string= self.connection_string,							
                            is_emulated=self.is_emulated)

    def is_azure_cosmosdb_table(self):
        return self.connection_string != None and "table.cosmosdb" in self.connection_string