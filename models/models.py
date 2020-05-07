import json
import os
import sys
import traceback

import config
import azure.common
from azure.storage import CloudStorageAccount
from table_crud import TableOperate , RecordOperate
from tablestorage_account import TableStorageAccount

account_connection_string = config.STORAGE_CONNECTION_STRING