import SocketServer
import NNTPComm
import socket

NEWSSERVER='pi.complete.org'
SERVERIP='127.0.0.1'
PORT=1178

class GopherRequest(SocketServer.BaseRequestHandler):
    def handle(self):
        print 'In handle'
        sock = self.request
        sf = sock.makefile("r+")
        req = sf.readline().strip().split("\t")[0][1:].split("/")
        ntc = NNTPComm.Server((SERVERIP, PORT), NEWSSERVER, sf)
        print "'%d'" % len(req)
        print req
        if (len(req) == 1 and req[0]):
            ngs = NNTPComm.Group(ntc, req[0])
            ngs.sendgrouplist()
        elif len(req) == 2 and req[1]:
            ngs = NNTPComm.Group(ntc, req[0])
            art = ngs.getmessage(req[1])
            art.display()
        else:
            ntc.sendnglist()
        print 'Handle: after if'
        sock.close()
        sf.close()
        print 'Handle: after close'

def Listen():
    server = SocketServer.TCPServer(('', PORT), GopherRequest)
    server.allow_reuse_address = 0
    server.serve_forever()
