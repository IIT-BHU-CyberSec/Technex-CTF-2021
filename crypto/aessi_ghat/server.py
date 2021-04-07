import os
import random
import socketserver
import threading
import time
from binascii import hexlify, unhexlify

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

from secret import flag

key = os.urandom(16)
iv = os.urandom(16)

class Handler(socketserver.StreamRequestHandler):
    def handle(self):
        try:
            cipher = AES.new(key, AES.MODE_OFB, iv)

            self.wfile.write(b'choice:')
            choice = self.rfile.readline(1).strip()

            if choice == b'1':
                self.request.sendall(b'Enter hex to encrypt:')
                data = unhexlify(self.rfile.readline(1024).strip())
                ret = cipher.encrypt(pad(data, 16))
                self.request.sendall(hexlify(ret))

            elif choice == b'2':
                self.request.sendall(b'Flag: ')
                ret = cipher.encrypt(pad(flag, 16))
                self.request.sendall(hexlify(ret))

        except:
            pass

        finally:
            self.request.sendall(b'\nbye!\n')

class MyThreadedServer(socketserver.ThreadingMixIn, socketserver.TCPServer, socketserver.DatagramRequestHandler):
    pass


class MyTCPServer(socketserver.TCPServer):
    pass

if __name__ == '__main__':
    PORT = 8000
    print('serving at PORT', PORT)
    server = MyThreadedServer(('0.0.0.0', PORT), Handler)
    server.allow_reuse_address = True

    server_thread = threading.Thread(target=server.serve_forever)

    server_thread.daemon = True
    server_thread.start()

    while True:
        time.sleep(20)
