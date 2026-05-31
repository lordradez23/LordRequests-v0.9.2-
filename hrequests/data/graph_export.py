'''
Knowledge Graph Export
~~~~~~~~~~~~~~~~~~~~~~

Exporting scraped data directly into RDF/GraphML formats for ingestion 
into graph databases like Neo4j.
'''

import json
from typing import List, Dict, Tuple

class GraphExporter:
    '''
    Converts list of entities and relationships into graph formats.
    '''
    def __init__(self):
        self.nodes: List[Dict] = []
        self.edges: List[Dict] = []

    def add_node(self, node_id: str, label: str, properties: Dict = None):
        self.nodes.append({
            "id": node_id,
            "label": label,
            "properties": properties or {}
        })

    def add_edge(self, source: str, target: str, relationship: str, properties: Dict = None):
        self.edges.append({
            "source": source,
            "target": target,
            "label": relationship,
            "properties": properties or {}
        })

    def to_graphml(self) -> str:
        '''
        Generates a basic GraphML string.
        '''
        xml = ['<?xml version="1.0" encoding="UTF-8"?>']
        xml.append('<graphml xmlns="http://graphml.graphdrawing.org/xmlns">')
        xml.append('  <graph id="G" edgedefault="directed">')
        
        for node in self.nodes:
            xml.append(f'    <node id="{node["id"]}" label="{node["label"]}"/>')
            
        for i, edge in enumerate(self.edges):
            xml.append(f'    <edge id="e{i}" source="{edge["source"]}" target="{edge["target"]}" label="{edge["label"]}"/>')
            
        xml.append('  </graph>')
        xml.append('</graphml>')
        return '\n'.join(xml)

    def to_json_lda(self) -> str:
        '''
        Generates a JSON-LD (Linked Data) representation.
        '''
        graph = []
        for node in self.nodes:
            item = {
                "@id": f"node:{node['id']}",
                "@type": node['label'],
                **node['properties']
            }
            graph.append(item)
            
        for edge in self.edges:
            # Finding source node to add relationship
            for item in graph:
                if item['@id'] == f"node:{edge['source']}":
                    item[edge['label']] = {"@id": f"node:{edge['target']}"}
                    
        return json.dumps({"@context": "http://schema.org", "@graph": graph}, indent=2)
