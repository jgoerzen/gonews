import SocketServer
import NNTPComm
import socket

NEWSSERVER='pi.complete.org'
SERVERIP='10.0.1.16'

class GopherRequest(SocketServer.BaseRequestHandler):
    def handle(self):
        sock = self.request
        sf = sock.makefile("r+")
        req = sf.readline().strip().split("\t")[0]
        ntc = NNTPComm.Server((SERVERIP, 1178), NEWSSERVER, sf)
        ntc.sendnglist()

def Listen():
    server = SocketServer.TCPServer(('', 1178), GopherRequest)
    server.allow_reuse_address = 0
    server.serve_forever()
