'''
Native SSH Tunneling.
Lets us use an SSH server as a proxy directly.
'''

import socket
import threading
import time
from typing import Optional

class SSHTunnel:
    '''
    Handles the local port forwarding stuff over SSH.
    Requires paramiko to be installed.
    '''
    def __init__(self, ssh_host: str, ssh_port: int, username: str, password: Optional[str] = None, key_path: Optional[str] = None):
        self.ssh_host = ssh_host
        self.ssh_port = ssh_port
        self.username = username
        self.password = password
        self.key_path = key_path
        self.local_port: Optional[int] = None
        self.is_active = False
        self._thread: Optional[threading.Thread] = None

    def start(self, remote_host: str = "127.0.0.1", remote_port: int = 80):
        '''
        Fires up the SSH tunnel in a background thread.
        '''
        try:
            import paramiko
        except ImportError:
            raise ImportError("You need to install 'paramiko' to use SSH tunnels.")

        def tunnel_proc():
            client = paramiko.SSHClient()
            client.load_system_host_keys()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            
            try:
                client.connect(
                    self.ssh_host, port=self.ssh_port,
                    username=self.username, password=self.password,
                    key_filename=self.key_path
                )
                
                # Find an open port on our machine to use for the tunnel
                sock = socket.socket()
                sock.bind(('', 0))
                self.local_port = sock.getsockname()[1]
                sock.close()
                
                with client.get_transport().open_channel(
                    "direct-tcpip", (remote_host, remote_port), ("127.0.0.1", self.local_port)
                ) as channel:
                    self.is_active = True
                    # Keep the tunnel open while we need it
                    while self.is_active:
                        time.sleep(1)
            except Exception as e:
                print(f"[SSH] Tunnel crashed: {e}")
            finally:
                self.is_active = False
                client.close()

        self._thread = threading.Thread(target=tunnel_proc, daemon=True)
        self._thread.start()
        
        # Give it a few seconds to grab a port before we bail
        timeout = 10
        while not self.local_port and timeout > 0:
            time.sleep(0.5)
            timeout -= 0.5
            
        return self.local_port

    def stop(self):
        '''Kills the tunnel.'''
        self.is_active = False
        if self._thread:
            self._thread.join()

    @property
    def proxy_url(self) -> Optional[str]:
        '''Returns the local proxy URL we can pass to requests.'''
        if self.local_port:
            return f"http://127.0.0.1:{self.local_port}"
        return None
