import sqlite3 
import json
import pandas

class Metadata:

    def __init__(self, table_name: str, schema: dict):
        self.table_name = table_name
        self.schema = schema


class WhiskyDb:
    
    def __init__(self):
        self.db_name = "whisky_db"
        self.meta_data_path = ""
        self._connection = self._init_db()
        self._cursor = self._connection.cursor()

    def _create_schema_from_metadata(self, metadata_path: str):
        with open(metadata_path) as f:
            metadata_raw = json.load(f)
            metadata = Metadata(metadata_raw["table_name"], metadata_raw["schema"])

        return metadata

    def _create_table_from_schema(self, metadata, cursor):
        sql = "CREATE TABLE IF NOT EXISTS {} ({})".format(metadata.table_name, metadata.schema)
        cursor.execute(sql)

    def _init_db(self):
        return sqlite3.connect(self.db_name, isolation_level=None)

    def _insert_from_csv(self, table_name, filepath, connection):
        df = pandas.read_csv(filepath)
        df.to_sql(table_name, connection, if_exists='append', index=None)





