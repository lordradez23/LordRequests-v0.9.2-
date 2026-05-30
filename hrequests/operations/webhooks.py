'''
Multi-Channel Alert Webhooks
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Provides a unified interface for sending operational alerts to 
Discord, Slack, and Telegram.
'''

import hrequests
import json
from typing import Optional

class AlertWebhooks:
    @staticmethod
    def send_discord_alert(webhook_url: str, content: str, title: str = "LordRequests Alert"):
        '''
        Sends a rich embed alert to Discord.
        '''
        payload = {
            "embeds": [{
                "title": title,
                "description": content,
                "color": 0x7289DA # Discord Blue
            }]
        }
        hrequests.post(webhook_url, json=payload)

    @staticmethod
    def send_slack_alert(webhook_url: str, text: str):
        '''
        Sends a simple text alert to Slack.
        '''
        payload = {"text": text}
        hrequests.post(webhook_url, json=payload)

    @staticmethod
    def send_telegram_alert(bot_token: str, chat_id: str, text: str):
        '''
        Sends a message via Telegram Bot API.
        '''
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        payload = {
            "chat_id": chat_id,
            "text": text,
            "parse_mode": "Markdown"
        }
        hrequests.post(url, json=payload)
