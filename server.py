import socket

class HTTP_Server:
    def run_server(self):
        s = self.init_socket()
        s.listen(5)
        print("Server is ready to receive a request")
        
        while True:
            (client, address) = s.accept()
            print(f"Received a connection from {address}")
            
            data = client.recv(1024)
            
            response = self.handle_request(data)
            
            client.sendall(response)
            client.close()
    
    
    def init_socket():
        # Sets up a TCP socket to listen on the HTTP port
        # param: None
        # return: The created socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('', 80))
        return s
    
    def handle_request(self, request):
        # Handle the request and return the response
        # param: request: The request data
        # return: The response data
        pass
