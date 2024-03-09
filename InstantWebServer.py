from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import os

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    FILE_DIRECTORY = r"D:\python"
    def do_GET(self):
        # Parse query parameters from URL
        parsed_url = urlparse(self.path)
        query_params = parse_qs(parsed_url.query)

        # Extract parameter value for 'id' key
        id_param = query_params.get('id', [''])[0]

        # Construct file name based on parameter value
        file_name = os.path.join(self.FILE_DIRECTORY, f"{id_param}.xml")        
        try:
            # Open and read the XML file
            with open(file_name, "rb") as file:
                file_content = file.read()

            # Set response status code
            self.send_response(200)

            # Set headers
            self.send_header('Content-type', 'text/xml')
            self.end_headers()

            # Send contents of XML file
            self.wfile.write(file_content)
        except FileNotFoundError:
            # If the file is not found, return a 404 error
            self.send_error(404, "File not found")

def run(server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler, port=8000):
    # Set server address and port
    server_address = ('', port)

    # Create server instance
    httpd = server_class(server_address, handler_class)

    # Start server
    print(f"Server started on port {port}")
    httpd.serve_forever()

# Run the server
if __name__ == '__main__':
    run()
