import os
import socket

class HTTP_Server:
    def run_server(self):
        # Runs the server and listens for incoming requests
        # The server will handle the requests and send back the responses
        s = self.init_socket()
        s.listen(5)
        print("Server is ready to receive a request")
        
        try:
            while True:
                (client, address) = s.accept()
                print(f"Received a connection from {address}")
                
                data = client.recv(1024)
                
                response = self.handle_request(data)
                
                client.sendall(response)
                client.close()
        except KeyboardInterrupt:
            print("Shutting down server.")
        finally:
            s.close()
    
    def init_socket(self):
        # Initializes the socket
        # The server will listen on port 80
        # returns: the socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('', 80))  # Use 80 for non-root testing
        return s
    
    def handle_request(self, request):
        # Handles the incoming request
        # request: the incoming request
        # returns: the response to send back to the client
        if request.startswith(b"GET"):
            return self.handle_get(request)
        else:
            return b"HTTP/1.1 501 Not Implemented\r\n\r\n"

    def handle_get(self, request):
        # Handles the GET request
        # request: the incoming request
        # returns: the response to send back to the client
        # Extracting the URI from the request line
        try:
            request_line = request.split(b'\r\n')[0]
            uri = request_line.split(b' ')[1]
            filename = uri.strip(b'/').decode()
        except Exception as e:
            return b"HTTP/1.1 400 Bad Request\r\n\r\n"

        # Handling file response
        if not os.path.exists(filename):
            response_line = b"HTTP/1.1 404 Not Found\r\n"
            response_headers = b"Content-Type: text/html\r\n\r\n"
            response_body = b"<h1>404 Not Found</h1>"
        else:
            response_line = b"HTTP/1.1 200 OK\r\n"
            response_headers = b"Content-Type: text/html\r\n"
            response_headers += b"Content-Length: " + str(os.path.getsize(filename)).encode() + b"\r\n\r\n"
            with open(filename, 'rb') as f:
                response_body = f.read()
        
        return b"".join([response_line, response_headers, response_body])

# Run the server
HTTP_Server().run_server()
