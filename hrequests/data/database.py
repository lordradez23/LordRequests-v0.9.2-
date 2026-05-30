'''
Database Export Pipeline
~~~~~~~~~~~~~~~~~~~~~~~~

Connectors for exporting scraped data to various database backends.
'''

import sqlite3
import csv
import json
from typing import List, Dict, Any, Optional

class DatabaseExporter:
    @staticmethod
    def to_csv(data: List[Dict[str, Any]], filename: str):
        if not data:
            return
        keys = data[0].keys()
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            dict_writer = csv.DictWriter(f, fieldnames=keys)
            dict_writer.writeheader()
            dict_writer.writerows(data)

    @staticmethod
    def to_json(data: List[Dict[str, Any]], filename: str):
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)

    @staticmethod
    def to_sqlite(data: List[Dict[str, Any]], db_path: str, table_name: str = 'scraped_data'):
        if not data:
            return
        
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Create table based on keys
        keys = list(data[0].keys())
        columns = ", ".join([f"{key} TEXT" for key in keys])
        cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({columns})")
        
        # Insert data
        placeholders = ", ".join(["?" for _ in keys])
        sql = f"INSERT INTO {table_name} VALUES ({placeholders})"
        
        rows = [tuple(str(d.get(k, '')) for k in keys) for d in data]
        cursor.executemany(sql, rows)
        
        conn.commit()
        conn.close()

    @staticmethod
    def to_mongodb(data: List[Dict[str, Any]], uri: str, db_name: str, collection_name: str):
        '''Export to MongoDB. Requires pymongo.'''
        try:
            from pymongo import MongoClient
            client = MongoClient(uri)
            db = client[db_name]
            collection = db[collection_name]
            collection.insert_many(data)
        except ImportError:
            print("pymongo is required for MongoDB export.")
