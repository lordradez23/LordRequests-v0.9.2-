'''
Dynamic CSS Class Resolver
~~~~~~~~~~~~~~~~~~~~~~~~~~

Logic to handle and identify highly obfuscated/randomized CSS classes
by analyzing element structure and neighboring relationships.
'''

from hrequests.parser import Element
from typing import List, Optional

class CSSResolver:
    '''
    Identifies elements based on structural patterns when class names are randomized.
    '''
    @staticmethod
    def find_by_structure(root: Element, tag: str, pattern: List[str]) -> List[Element]:
        '''
        Finds elements of a specific tag that have a specific sequence of child tags.
        pattern: list of tags (e.g. ['span', 'i', 'div'])
        '''
        candidates = root.find_all(tag)
        matches = []
        
        for cand in candidates:
            # Check direct children tags
            children = cand.element.iter()
            child_tags = [c.tag for c in children if c.tag != tag] # Filter out the parent tag if it appears in iter
            
            if len(child_tags) >= len(pattern):
                # Simple subsequence check
                if all(p in child_tags for p in pattern):
                    matches.append(cand)
                    
        return matches

    @staticmethod
    def identify_stable_parent(element: Element, depth: int = 3) -> Optional[Element]:
        '''
        Travels up the DOM tree to find a parent with a likely stable ID or class.
        '''
        current = element
        for _ in range(depth):
            if not hasattr(current.element, 'parent'):
                break
            parent_node = current.element.parent
            if not parent_node:
                break
            
            # Re-wrap in hrequests Element
            parent = Element(element=parent_node, url=current.url, br_session=current.br_session)
            
            # Check if parent has a 'clean' looking ID (no long random strings)
            p_id = parent.attrs.get('id', '')
            if p_id and len(p_id) < 20 and not any(c.isdigit() for c in p_id):
                return parent
                
            current = parent
        return None
