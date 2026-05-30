'''
Auto-Table Extractor
~~~~~~~~~~~~~~~~~~~~

Detects and extracts HTML tables from a page, converting them 
into structured formats like CSV or lists.
'''

import hrequests
import csv
from typing import List, Dict

class TableExtractor:
    def __init__(self, response: hrequests.response.Response):
        self.response = response
        self.html = response.html

    def extract_all(self) -> List[List[List[str]]]:
        '''
        Finds all <table> elements and parses them into nested lists.
        '''
        tables = []
        for table_el in self.html.find('table'):
            current_table = []
            for row in table_el.find('tr'):
                # Extract headers (th) and data (td)
                cells = [cell.text.strip() for cell in row.find('th, td')]
                if cells:
                    current_table.append(cells)
            if current_table:
                tables.append(current_table)
        return tables

    def save_to_csv(self, table_index: int, filepath: str):
        '''
        Saves a specific table to a CSV file.
        '''
        tables = self.extract_all()
        if table_index >= len(tables):
            print(f"Table index {table_index} not found.")
            return

        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerows(tables[table_index])
        print(f"Table {table_index} saved to {filepath}")
