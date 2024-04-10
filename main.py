import os
import http.server
import socketserver
import threading

# Replace with the directory where uploaded files will be saved
UPLOAD_DIR = "uploads"

class UploadHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        file_content = self.rfile.read(content_length)

        filename = self.headers['filename'] 
        filepath = os.path.join(UPLOAD_DIR, filename)

        # Save the uploaded file
        with open(filepath, 'wb') as f:
            f.write(file_content)

        # Log server details
        print(f"\nIncoming request from: {self.client_address[0]}")
        print(f"Request method: {self.command}")
        print(f"Request path: {self.path}")
        print(f"Outgoing response to: {self.client_address[0]}")
        print(f"Response status code: 201")
        print(f"Response headers: {self.headers}")
        print(f"Uploaded file: {filename}")

        self.send_response(201)
        self.end_headers()
        self.wfile.write("File uploaded successfully".encode())

class ThreadedHTTPServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    pass

if __name__ == '__main__':
    # Create the upload directory if it doesn't exist
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    # Set up the threaded HTTP server
    server_address = ('', 1001)
    httpd = ThreadedHTTPServer(server_address, UploadHandler)

    # Start a new thread for the server
    server_thread = threading.Thread(target=httpd.serve_forever)
    server_thread.daemon = True  
    server_thread.start()

    print('Server started.')
    
    # Wait for the server thread to finish (Ctrl+C to stop)
    try:
        server_thread.join()
    except KeyboardInterrupt:
        print('Server stopped.')
