'''
Auto-Schema Discovery
~~~~~~~~~~~~~~~~~~~~~

Dynamic mapping of nested API responses to structured data schemas.
'''

import json
from typing import Dict, Any, List, Set

class SchemaDiscoverer:
    '''
    Infers data types and structures from JSON responses.
    '''
    def __init__(self):
        self.schema: Dict[str, str] = {}

    def discover(self, data: Any, prefix: str = "") -> Dict[str, str]:
        '''
        Recursively maps a JSON object to a flat schema with types.
        '''
        if isinstance(data, dict):
            for key, val in data.items():
                new_prefix = f"{prefix}.{key}" if prefix else key
                self.discover(val, new_prefix)
        elif isinstance(data, list):
            if data:
                self.discover(data[0], f"{prefix}[]")
            else:
                self.schema[prefix] = "List[Empty]"
        else:
            self.schema[prefix] = type(data).__name__
            
        return self.schema

    def to_sql_ddl(self, table_name: str) -> str:
        '''
        Generates a basic SQL CREATE TABLE statement based on the discovered schema.
        '''
        columns = []
        for path, dtype in self.schema.items():
            # Clean up path for SQL names
            col_name = path.replace('.', '_').replace('[]', '_list')
            sql_type = "TEXT"
            if dtype == 'int': sql_type = "INTEGER"
            elif dtype == 'float': sql_type = "REAL"
            columns.append(f"    {col_name} {sql_type}")
            
        return f"CREATE TABLE {table_name} (\n" + ",\n".join(columns) + "\n);"
