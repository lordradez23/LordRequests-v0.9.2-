'''
RSS Feed Generator
~~~~~~~~~~~~~~~~~~

Converts dynamic web results into standard RSS/Atom feeds for tracking.
'''

import time
from typing import List, Dict

class RSSGenerator:
    @staticmethod
    def generate_rss(title: str, description: str, link: str, items: List[Dict]) -> str:
        '''
        Generates a basic RSS 2.0 XML string.
        items: [{'title': '...', 'link': '...', 'description': '...'}]
        '''
        rss = f'''<?xml version="1.0" encoding="UTF-8" ?>
<rss version="2.0">
<channel>
 <title>{title}</title>
 <description>{description}</description>
 <link>{link}</link>
 <lastBuildDate>{time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.gmtime())}</lastBuildDate>
'''
        for item in items:
            rss += f''' <item>
  <title>{item.get('title', 'No Title')}</title>
  <link>{item.get('link', '')}</link>
  <description>{item.get('description', '')}</description>
  <pubDate>{time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.gmtime())}</pubDate>
 </item>
'''
        rss += "</channel>\n</rss>"
        return rss

    @staticmethod
    def save_feed(rss_content: str, filepath: str):
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(rss_content)
        print(f"RSS feed saved to {filepath}")
