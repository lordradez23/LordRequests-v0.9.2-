'''
Sentiment Pattern Analyzer
~~~~~~~~~~~~~~~~~~~~~~~~~~

Real-time sentiment scoring of extracted text content using a rule-based engine.
'''

from typing import Dict, List
import re

class SentimentAnalyzer:
    '''
    Analyzes text for positive/negative sentiment using keyword heuristics.
    '''
    POSITIVE_WORDS = {
        'great', 'awesome', 'excellent', 'happy', 'good', 'success', 'winning',
        'profit', 'growth', 'best', 'perfect', 'reliable', 'trust', 'safe'
    }
    NEGATIVE_WORDS = {
        'bad', 'awful', 'terrible', 'sad', 'fail', 'loss', 'error', 'scam',
        'fraud', 'danger', 'risk', 'avoid', 'broken', 'poor', 'expensive'
    }

    @classmethod
    def analyze(cls, text: str) -> Dict[str, any]:
        '''
        Calculates sentiment score and returns breakdown.
        '''
        words = re.findall(r'\w+', text.lower())
        if not words:
            return {"score": 0, "label": "neutral", "matches": 0}

        pos_count = sum(1 for w in words if w in cls.POSITIVE_WORDS)
        neg_count = sum(1 for w in words if w in cls.NEGATIVE_WORDS)
        
        total_matches = pos_count + neg_count
        if total_matches == 0:
            return {"score": 0, "label": "neutral", "matches": 0}

        score = (pos_count - neg_count) / total_matches
        
        label = "neutral"
        if score > 0.2:
            label = "positive"
        elif score < -0.2:
            label = "negative"
            
        return {
            "score": round(score, 2),
            "label": label,
            "positive_count": pos_count,
            "negative_count": neg_count,
            "total_words": len(words)
        }

    @classmethod
    def batch_analyze(cls, texts: List[str]) -> List[Dict]:
        return [cls.analyze(t) for t in texts]
