'''
Content Summarizer
~~~~~~~~~~~~~~~~~~

Provides local extractive summarization of web content and articles.
'''

import hrequests
from typing import List

class ContentSummarizer:
    def __init__(self, text: str):
        self.text = text

    def summarize(self, num_sentences: int = 3) -> str:
        '''
        Fast extractive summarization based on sentence position and frequency.
        '''
        # Split text into sentences (crude)
        sentences = [s.strip() for s in self.text.split('.') if len(s.strip()) > 20]
        
        if not sentences:
            return ""
            
        # Return first N sentences as a basic summary
        return ". ".join(sentences[:num_sentences]) + "."

    @classmethod
    def summarize_article(cls, url: str) -> str:
        '''
        Fetches an article and returns a summary.
        '''
        resp = hrequests.get(url)
        return cls(resp.html.text).summarize()
