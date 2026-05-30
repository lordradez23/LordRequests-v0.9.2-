'''
Interactive REPL Shell
~~~~~~~~~~~~~~~~~~~~~~

Custom interactive request shell for LordRequests.
'''

import code
import sys
import hrequests

class LordShell:
    def __init__(self):
        self.namespace = {
            'hrequests': hrequests,
            'hr': hrequests,
            'get': hrequests.get,
            'post': hrequests.post,
            'Session': hrequests.Session,
            'BrowserSession': hrequests.BrowserSession,
        }
        self.banner = (
            "================================================\n"
            "   LordRequests (v0.9.2) Interactive Shell      \n"
            "================================================\n"
            "Pre-imported: hrequests (as hr), get, post, Session\n"
            "Type exit() or Ctrl+D to quit.\n"
        )

    def start(self):
        # Add basic autocomplete if available
        try:
            import readline
            import rlcompleter
            readline.set_completer(rlcompleter.Completer(self.namespace).complete)
            readline.parse_and_bind("tab: complete")
        except ImportError:
            pass

        shell = code.InteractiveConsole(self.namespace)
        shell.interact(banner=self.banner, exitmsg="Goodbye.")

if __name__ == "__main__":
    LordShell().start()
