import http.server
import socketserver
import socket
import os
import time

def find_free_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))
        s.listen(1)
        port = s.getsockname()[1]
    return port

def run_server():
    PORT = 8000
    Handler = http.server.SimpleHTTPRequestHandler

    # Try using port 8000 first, if not available use a random port
    try:
        httpd = socketserver.TCPServer(("", PORT), Handler)
    except OSError:
        PORT = find_free_port()
        httpd = socketserver.TCPServer(("", PORT), Handler)

    print(f"Server running at http://localhost:{PORT}")
    print(f"Access the Greek Recipes at: http://localhost:{PORT}/greek_recipes.html")
    print(f"Access the Career Quiz at: http://localhost:{PORT}/career_quiz.html")
    print("Press Ctrl+C to stop the server")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped")
        httpd.server_close()

if __name__ == "__main__":
    run_server() 