'''
Phantom Mirroring
~~~~~~~~~~~~~~~~~

Advanced content extraction and sanitization for archival and
censorship-resistant mirroring.
'''

import re
from typing import Dict, List, Optional
import hrequests

class PhantomMirror:
    def __init__(self, response: hrequests.response.Response):
        self.response = response
        self.html = response.html
        self.metadata: Dict = {}

    def extract_article(self) -> Dict:
        '''
        Extracts the main content of an article, including title and text.
        '''
        # Basic heuristic for title
        title = self.html.find('title', first=True)
        self.metadata['title'] = title.text if title else "No Title"

        # Basic heuristic for main content
        # Usually inside <article>, <main>, or a div with much text
        body = self.html.find('article', first=True) or \
               self.html.find('main', first=True) or \
               self.html.find('body', first=True)
        
        # Strip scripts and styles
        if body:
            content = body.text
        else:
            content = self.response.text

        self.metadata['content'] = content
        self.metadata['url'] = self.response.url
        self.metadata['timestamp'] = self.response.elapsed # Placeholder
        
        return self.metadata

    def sanitize_links(self) -> List[str]:
        '''
        Returns all absolute links on the page, sanitized.
        '''
        return list(self.html.absolute_links)

    def prepare_archive(self, output_path: str):
        '''
        Saves a sanitized markdown-like archive of the page.
        '''
        article = self.extract_article()
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(f"# {article['title']}\n")
            f.write(f"Source: {article['url']}\n")
            f.write("-" * 20 + "\n\n")
            f.write(article['content'])
        
        print(f"Archive saved to {output_path}")
