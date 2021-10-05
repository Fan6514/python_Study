import socket
import time

start = time.time()
# create a socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# create a connection
s.connect(('127.0.0.1', 9999))
print(s.recv(1024).decode('utf-8'))
for data in [b'Michael', b'Tracy', b'Sarah']:
    # send data
    s.send(data)
    print(s.recv(1024).decode('utf-8'))
s.send(b'exit')
s.close()
elapsed = float(time.time() - start)
print('completed in %0.3f seconds\n' % elapsed)