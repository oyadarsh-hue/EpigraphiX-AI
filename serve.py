#!/usr/bin/env python3
"""
EpigraphiX-AI Web Studio Localhost Server Launcher
Starts a local HTTP server serving the web_studio directory and opens the browser automatically.
"""

import sys
import os
import socket
import webbrowser
import threading
import time
from http.server import SimpleHTTPRequestHandler
try:
    from http.server import ThreadingHTTPServer as HTTPServerClass
except ImportError:
    from http.server import HTTPServer as HTTPServerClass

def is_port_in_use(port):
    """Check if a port is already occupied."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(0.5)
        try:
            s.bind(("0.0.0.0", port))
            return False
        except OSError:
            return True

def find_available_port(start_port=8080, max_attempts=20):
    """Find an available port starting from start_port."""
    for port in range(start_port, start_port + max_attempts):
        if not is_port_in_use(port):
            return port
    return start_port

def open_browser(url):
    """Wait briefly for server to bind and open browser."""
    time.sleep(0.8)
    print(f"[*] Opening browser at {url} ...")
    try:
        webbrowser.open(url)
    except Exception as e:
        print(f"[!] Could not launch browser automatically: {e}")

def main():
    # Resolve absolute directory of web_studio
    script_dir = os.path.dirname(os.path.abspath(__file__))
    web_studio_dir = os.path.join(script_dir, "web_studio")

    if not os.path.exists(web_studio_dir):
        # Fallback if running from within web_studio
        if os.path.exists(os.path.join(script_dir, "index.html")):
            web_studio_dir = script_dir
        else:
            print(f"[!] Error: Could not find web_studio directory at: {web_studio_dir}")
            sys.exit(1)

    preferred_port = 8080
    if len(sys.argv) > 1:
        try:
            preferred_port = int(sys.argv[1])
        except ValueError:
            pass

    port = find_available_port(preferred_port)
    server_url = f"http://localhost:{port}"

    class CustomHandler(SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=web_studio_dir, **kwargs)

        def end_headers(self):
            self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate, max-age=0')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Expires', '0')
            super().end_headers()
            
        def log_message(self, format, *args):
            sys.stdout.write(f"[{self.log_date_time_string()}] {format % args}\n")
            sys.stdout.flush()

    print("=" * 65)
    print(" [EpigraphiX-AI] Neural Palm-Leaf OCR Web Studio Server")
    print("=" * 65)
    print(f" [*] Web Directory : {web_studio_dir}")
    print(f" [*] Localhost URL : {server_url}")
    print("=" * 65)
    print(" [OK] Server is LIVE and RUNNING.")
    print(" [OK] Press Ctrl + C in this terminal window to stop the server.")
    print("=" * 65)

    # Launch browser in background thread
    threading.Thread(target=open_browser, args=(server_url,), daemon=True).start()

    try:
        server = HTTPServerClass(("0.0.0.0", port), CustomHandler)
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n\n[!] Server stopped by user. Goodbye!")
        try:
            server.shutdown()
        except Exception:
            pass
        sys.exit(0)
    except Exception as e:
        print(f"\n[!] Server error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
