'''
Secure Web-UI Dashboard
~~~~~~~~~~~~~~~~~~~~~~~

A local web interface for monitoring and controlling LordRequests operations.
'''

import hrequests
import threading
from typing import Optional
try:
    from flask import Flask, jsonify, render_template_string
except ImportError:
    Flask = None

class WebDashboard:
    '''
    Spawns a local Flask server to provide a web-based monitoring dashboard.
    '''
    def __init__(self, port: int = 5001):
        self.port = port
        self.app = Flask(__name__) if Flask else None
        self._setup_routes()
        self.is_running = False

    def _setup_routes(self):
        if not self.app:
            return

        @self.app.route('/')
        def index():
            return render_template_string("""
            <html>
                <head><title>LordRequests Dashboard</title></head>
                <body style="background: #121212; color: #e0e0e0; font-family: sans-serif; padding: 20px;">
                    <h1>LordRequests Live Operations</h1>
                    <div id="stats" style="border: 1px solid #333; padding: 15px; border-radius: 8px;">
                        <p>Status: <span style="color: #4caf50;">ACTIVE</span></p>
                        <ul id="stats-list"></ul>
                    </div>
                </body>
            </html>
            """)

        @self.app.route('/api/stats')
        def stats():
            from hrequests.operations.dashboard import DashboardStats
            return jsonify({
                "total_requests": DashboardStats.total_requests,
                "success_ratio": (DashboardStats.successful_requests / (DashboardStats.total_requests or 1)) * 100,
                "active_sessions": DashboardStats.active_sessions
            })

    def start(self):
        if not self.app:
            print("[WebUI] Flask is not installed. Web dashboard unavailable.")
            return

        self.is_running = True
        thread = threading.Thread(target=lambda: self.app.run(port=self.port, use_reloader=False), daemon=True)
        thread.start()
        print(f"[WebUI] Dashboard started at http://localhost:{self.port}")
