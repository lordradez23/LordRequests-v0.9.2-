'''
Knowledge Graph Linker
~~~~~~~~~~~~~~~~~~~~~~

Formatting and linking extracted entities for Graph Database ingestion.
'''

import json
from typing import List, Dict, Tuple

class GraphLinker:
    '''
    Structures data as Subject-Predicate-Object triples.
    '''
    def __init__(self):
        self.triples: List[Tuple[str, str, str]] = []

    def add_relationship(self, subject: str, predicate: str, obj: str):
        '''
        Adds a new edge to the local graph.
        '''
        self.triples.append((subject, predicate, obj))

    def to_json_ld(self) -> str:
        '''
        Exports the graph as a basic JSON-LD structure.
        '''
        nodes = []
        for s, p, o in self.triples:
            nodes.append({
                "@id": f"resource:{s.replace(' ', '_')}",
                p: o
            })
        return json.dumps({"@context": "http://schema.org/", "@graph": nodes}, indent=2)

    def to_cypher(self, label: str = "Node") -> str:
        '''
        Generates basic Neo4j Cypher MERGE statements.
        '''
        statements = []
        for s, p, o in self.triples:
            s_clean = s.replace("'", "\\'")
            o_clean = o.replace("'", "\\'")
            statements.append(
                f"MERGE (a:{label} {{name: '{s_clean}'}}) "
                f"MERGE (b:{label} {{name: '{o_clean}'}}) "
                f"MERGE (a)-[:{p.upper()}]->(b);"
            )
        return "\n".join(statements)
