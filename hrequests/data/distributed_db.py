'''
Distributed Database Connector
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Native support for CockroachDB, Cassandra, and distributed MongoDB for large-scale scrapes.
'''

from typing import Dict, List, Optional, Any

class DistributedDBConnector:
    '''
    Standardized interface for interacting with distributed databases.
    '''
    def __init__(self, db_type: str, connection_string: str):
        self.db_type = db_type.lower()
        self.conn_str = connection_string
        self.client: Any = None
        self._connected = False

    def connect(self):
        '''
        Initializes the driver based on db_type.
        '''
        try:
            if self.db_type == 'mongodb':
                import pymongo
                self.client = pymongo.MongoClient(self.conn_str)
            elif self.db_type == 'cockroachdb' or self.db_type == 'postgres':
                import psycopg2
                self.client = psycopg2.connect(self.conn_str)
            elif self.db_type == 'cassandra':
                from cassandra.cluster import Cluster
                self.client = Cluster([self.conn_str]).connect()
            self._connected = True
        except ImportError as e:
            print(f"[DB] Driver missing for {self.db_type}: {e}")
        except Exception as e:
            print(f"[DB] Connection failed: {e}")

    def insert_record(self, table: str, record: Dict):
        '''
        Inserts a single record into the database.
        '''
        if not self._connected:
            self.connect()
        
        if self.db_type == 'mongodb':
            self.client.get_database()[table].insert_one(record)
        elif self.db_type in ['cockroachdb', 'postgres']:
            with self.client.cursor() as cur:
                # Simplified insert logic
                keys = ",".join(record.keys())
                values = ",".join(["%s"] * len(record))
                cur.execute(f"INSERT INTO {table} ({keys}) VALUES ({values})", list(record.values()))
                self.client.commit()
        print(f"[DB] Record inserted into {table}.")
