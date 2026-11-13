import os
import re
import sys
import socket
from http.server import SimpleHTTPRequestHandler, HTTPServer

class RangeRequestHandler(SimpleHTTPRequestHandler):
    def guess_type(self, path):
        # Explicitly guarantee correct mime types on Windows registry issues
        if path.endswith('.mp4'):
            return 'video/mp4'
        if path.endswith('.css'):
            return 'text/css'
        if path.endswith('.js'):
            return 'application/javascript'
        if path.endswith('.html'):
            return 'text/html'
        return super().guess_type(path)

    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, HEAD, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Range, Content-Type")
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200, "OK")
        self.end_headers()

    def send_head(self):
        """Common code for GET and HEAD commands.
        This sends the response code and headers.
        """
        path = self.translate_path(self.path)
        f = None
        if os.path.isdir(path):
            return super().send_head()
            
        ctype = self.guess_type(path)
        try:
            f = open(path, 'rb')
        except OSError:
            self.send_error(404, "File not found")
            return None

        # Check for Range header
        range_header = self.headers.get('Range')
        if not range_header:
            return super().send_head()

        # Parse range header (e.g., 'bytes=0-1000' or 'bytes=1000-')
        match = re.match(r'bytes=(\d+)-(\d*)', range_header)
        if not match:
            self.send_error(400, "Bad Request (invalid Range header)")
            f.close()
            return None

        fs = os.fstat(f.fileno())
        file_len = fs.st_size
        
        start = int(match.group(1))
        end = match.group(2)
        if end:
            end = int(end)
        else:
            end = file_len - 1

        if start >= file_len:
            self.send_response(416, "Requested Range Not Satisfiable")
            self.send_header("Content-Range", f"bytes */{file_len}")
            self.end_headers()
            f.close()
            return None

        end = min(end, file_len - 1)
        self.range_start = start
        self.range_end = end
        
        content_length = end - start + 1
        
        self.send_response(206, "Partial Content")
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(content_length))
        self.send_header("Content-Range", f"bytes {start}-{end}/{file_len}")
        self.send_header("Accept-Ranges", "bytes")
        self.end_headers()
        return f

    def copyfile(self, source, outputfile):
        """Copy block-by-block if range is set, else call super."""
        if hasattr(self, 'range_start') and hasattr(self, 'range_end'):
            source.seek(self.range_start)
            bytes_to_send = self.range_end - self.range_start + 1
            buffer_size = 64 * 1024
            while bytes_to_send > 0:
                try:
                    chunk = source.read(min(bytes_to_send, buffer_size))
                    if not chunk:
                        break
                    outputfile.write(chunk)
                    bytes_to_send -= len(chunk)
                except (ConnectionAbortedError, ConnectionResetError):
                    # Browser closed connection (e.g. paused/seeked), exit gracefully
                    break
        else:
            super().copyfile(source, outputfile)

class DualStackHTTPServer(HTTPServer):
    address_family = socket.AF_INET6
    
    def server_bind(self):
        self.socket.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, 0)
        super().server_bind()

if __name__ == '__main__':
    port = 3000
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    
    server_address = ('', port)
    httpd = DualStackHTTPServer(server_address, RangeRequestHandler)
    print(f"Starting custom dual-stack range HTTP server on port {port}...")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server...")
        httpd.server_close()
