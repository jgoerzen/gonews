import nntplib
import types

class Server:
    def __init__(self, myaddr, nntpserver, destfile):
        self.myaddr = myaddr
        self.nntpservername = nntpserver
        self.outfile = destfile
        self.server = nntplib.NNTP(nntpserver)

    def sendnglist(self):
        for group in map(lambda x: x[0], self.server.list()[1]):
            self.outfile.write("1%s\t/%s\t%s\t%s\n" % \
                               (group, group, self.myaddr[0],
                                self.myaddr[1]))

    def getoutfile(self):
        return self.outfile

    def getnntp(self):
        return self.server

class Group:
    def __init__(self, server, group):
        self.server = server
        self.groupname = group
        self.messages = []
        self.start = None
        self.end = None
        
    def getmessages(self, start=None, end=None):
        if self.messages:
            return self.messages
        nntp = self.server.getnntp()
        groupinfo = nntp.group(self.groupname)
        self.start = groupinfo[2]
        self.end = groupinfo[3]
        if start == None: start = self.start
        if end == None: end = self.end

        for xover in nntp.xover(start, end)[1]:
            self.messages.append(Message(self, xover))

        return self.messages

    def getmessage(self, number):
        return Message(self, number)

    def entergroup(self):
        return self.server.getnntp().group(self.groupname)

    def sendgrouplist(self):
        self.getmessages()
        for message in self.messages:
            self.server.outfile.write(message.getgopherlink())

class Message:
    def __init__(self, group, xoverdata):
        self.group = group
        self.server = group.server
        if type(xoverdata) == types.TupleType:
            self.xoverdata = xoverdata
            self.number = xoverdata[0]
            self.subject = xoverdata[1]
            self.poster = xoverdata[2]
            self.date = xoverdata[3]
            self.id = xoverdata[4]
            self.references = xoverdata[5]
            self.size = xoverdata[6]
            self.lines = xoverdata[7]
        else:
            self.number = xoverdata

    def getgopherlink(self):
        return "0[ %-20s ] %s\t%s\t%s\t%s\n" % (
            self.poster, self.subject,
            "/" + self.group.groupname + "/" + self.number,
            self.server.myaddr[0],
            self.server.myaddr[1])
    
    def display(self):
        self.group.entergroup()
        lines = self.server.getnntp().article(self.number)[3]
        [self.server.outfile.write(line + "\n") for line in lines]
