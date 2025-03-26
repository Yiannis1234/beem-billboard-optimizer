import http.server
import socketserver
import os
import sys

PORT = 8000
Handler = http.server.SimpleHTTPRequestHandler

def find_free_port(start_port):
    port = start_port
    max_port = start_port + 100
    
    while port < max_port:
        try:
            with socketserver.TCPServer(("", port), Handler) as httpd:
                httpd.server_close()
                return port
        except OSError:
            port += 1
    
    return None

if __name__ == "__main__":
    try:
        # Check if port 8000 is already in use
        try:
            with socketserver.TCPServer(("", PORT), Handler) as test_server:
                test_server.server_close()
        except OSError:
            # Find a free port
            PORT = find_free_port(8001)
            if PORT is None:
                print("Could not find a free port. Please close some applications and try again.")
                sys.exit(1)
        
        print(f"Serving at http://localhost:{PORT}")
        with socketserver.TCPServer(("", PORT), Handler) as httpd:
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
        sys.exit(0) 