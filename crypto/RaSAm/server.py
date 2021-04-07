import os
import random
import socketserver
import threading
import time
from binascii import hexlify, unhexlify

from Crypto.PublicKey import RSA
from Crypto.Util.number import long_to_bytes, bytes_to_long

from secret import flag, p, q, e, d

key = RSA.construct((p*q, e, d, p, q))

class Handler(socketserver.StreamRequestHandler):
    def send_flag(self, key: RSA.RsaKey, flag: bytes):
        m = bytes_to_long(flag)
        self.wfile.write(f'n={key.n}\n'.encode())
        self.wfile.write(f'e={key.e}\n'.encode())
        self.wfile.write(b'here is your flag')
        self.wfile.write(hex(pow(m, key.e, key.n)).encode())

    def decrypt(self, key: RSA.RsaKey, cipher: bytes):
        c = bytes_to_long(cipher)
        m = str(key._decrypt(c) &1)
        self.wfile.write(m.encode())

    def handle(self):
        self.wfile.write(b'Your Choice:')
        try:
            choice = self.rfile.readline().strip()

            if choice == b'2':
                self.wfile.write(b'\nEnter hex to decrypt:')
                data = self.rfile.readline().strip()
                self.decrypt(key, unhexlify(data))

            elif choice == b'1':
                self.send_flag(key, flag)

        except:
            pass

        finally:
            self.wfile.write(b'\nbye!\n')

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
