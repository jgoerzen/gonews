import nntplib

class Server:
    def __init__(self, myaddr, nntpserver, destfile):
        self.myaddr = myaddr
        self.nntpservername = nntpserver
        self.outfile = destfile
        self.server = nntplib.NNTP(nntpserver)

    def sendnglist(self):
        for group in map(lambda x: x[0], self.server.list()[1]):
            self.outfile.write("1%s\t%s\t%s\t%s\n" % \
                               (group, group, self.myaddr[0],
                                self.myaddr[1]))
