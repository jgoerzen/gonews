import SocketServer
import NNTPComm
import socket

NEWSSERVER='pi.complete.org'
SERVERIP='10.0.1.16'

class GopherRequest(SocketServer.BaseRequestHandler):
    def handle(self):
        sock = self.request
        sf = sock.makefile("r+")
        req = sf.readline().strip().split("\t")
        ntc = NNTPComm.Server((SERVERIP, 1176), NEWSSERVER, sf)
        if (req[0]):
            ngs = NNTPComm.Group(ntc, req[0])
            ngs.sendgrouplist()
        else:
            ntc.sendnglist()

def Listen():
    server = SocketServer.TCPServer(('', 1176), GopherRequest)
    server.allow_reuse_address = 0
    server.serve_forever()
