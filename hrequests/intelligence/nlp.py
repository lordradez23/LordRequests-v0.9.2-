'''
NLP Topic Clustering
~~~~~~~~~~~~~~~~~~~~

Semantic grouping of scraped text content based on keyword frequency.
'''

from collections import Counter
from typing import List, Dict, Set
import re

class TopicClusturer:
    '''
    Groups documents into topical clusters using keyword analysis.
    '''
    def __init__(self, stopwords: Optional[Set[str]] = None):
        self.stopwords = stopwords or {'the', 'and', 'for', 'with', 'that', 'this', 'from'}

    def _extract_keywords(self, text: str, limit: int = 5) -> List[str]:
        '''
        Extracts the most frequent non-stopword tokens from a string.
        '''
        words = re.findall(r'\b\w{4,}\b', text.lower())
        meaningful = [w for w in words if w not in self.stopwords]
        counts = Counter(meaningful)
        return [word for word, count in counts.most_common(limit)]

    def cluster_documents(self, documents: List[str]) -> Dict[str, List[int]]:
        '''
        Groups document indices by their primary keyword.
        '''
        clusters = {}
        for idx, doc in enumerate(documents):
            keywords = self._extract_keywords(doc, limit=1)
            topic = keywords[0] if keywords else "uncategorized"
            
            if topic not in clusters:
                clusters[topic] = []
            clusters[topic].append(idx)
        return clusters

    @staticmethod
    def get_summary(text: str) -> str:
        '''Returns a very basic summary (first sentence).'''
        sentences = text.split('.')
        return (sentences[0] + '.') if sentences else ""
