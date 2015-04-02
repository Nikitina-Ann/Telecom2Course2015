__author__ = 'Аня'
'''import socket
class MockSocket(socket.socket):
    def recv(self, bufsize):
        pass
    def send(self, data, flags=None):
        socket.socket.send(b'220\r\n')

port=11000
sock=MockSocket('AF_INET', 'SOCK_STREAM')
sock.bind(('localhost', port))
sock.listen(3)
while(1):
    conn, addr = sock.accept()'''
