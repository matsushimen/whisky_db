import sqlite3 
import json


class WhiskyDb:
    
    def __init__(self):
        self.db_name = "whisky_db"
        self.meta_whisky_path = ""
        self.meta_distillary_path = ""
        self.meta_owner_path = ""

    def _create_schema_from_metadata(self, metadata_path: str):
        with open(metadata_path, "r") as meta:
            metadata = ""

        return metadata


    def _create_table_from_schema(self, metadata, cursor):
        sql = f"CREATE TABLE IF NOT EXISTS {} ({})".format(metadata.table_name, metadata.schema)
        cursor.execute(sql)

    def _init_db(self):
        connection = sqlite3.connect(self.db_name, isolation_level=None)

