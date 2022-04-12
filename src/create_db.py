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
        self.metadata_path = "data/meta/schema.json"
        self._connection = self._init_db()
        self._cursor = self._connection.cursor()

    def _create_metadata_from_json(self, metadata_path: str):
        metas = []
        with open(metadata_path) as f:
            metadata_raw = json.load(f)
            for table in  metadata_raw.keys():
                metas.append(Metadata(table, metadata_raw[table]))

        return metas

    def _create_table_from_metadata(self, metas, cursor):
        initial_db = 'id INTEGER PRIMARY KEY'
        for metadata in metas:
            cursor.execute("CREATE TABLE IF NOT EXISTS {} ({})".format(metadata.table_name, initial_db))
            for k, v in metadata.schema.items():
                cursor.sql("ALTER TABLE {} ADD {} {}".format(metadata.table_name, k, v))

    def _init_db(self):
        return sqlite3.connect(self.db_name, isolation_level=None)

    def _insert_from_csv(self, table_name, filepath, connection):
        df = pandas.read_csv(filepath)
        df.to_sql(table_name, connection, if_exists='append', index=None)

    def create_db(self):
        metas = self._create_metadata_from_json(self.metadata_path)
        self._create_table_from_metadata(metas, self._cursor)

    def close(self):
        self._connection.close()
        self._cursor.close()

if __name__ == '__main__':
    db = WhiskyDb()
    db.create_db()
    db.close()



