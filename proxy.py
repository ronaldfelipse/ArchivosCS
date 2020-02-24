import zmq
import threading


ps =  1024*1024*2
Servers = []

context = zmq.Context()

def Bdecode(bToEncode):
    return bToEncode.decode("utf-8")

def Strencode(strToEncode):
    return str(strToEncode).encode("utf-8")

def FirstConex():
    return ([Strencode(len(Servers)),Strencode(ps)])

def UploadFile(FileName):
    DataServer = Servers[0].split(":")
    return ([b"1",Strencode(DataServer[0]),Strencode(DataServer[1]) ] )

def NewServerON(Direccion,Puerto):
    
        global Servers
        Servers.append(Direccion+":"+Puerto)
    
    
def ListenServers():
    
        global context
    
        socketServers = context.socket(zmq.REP)
        socketServers.bind("tcp://*:8855")
        
        while True:
            MSJData = socketServers.recv_multipart()

            Type = Bdecode(MSJData[0])

            if Type == "0" :
                 NewServerON(Bdecode(MSJData[1]),Bdecode(MSJData[2]))

            socketServers.send_multipart([b"1"]) 


def init():
    
        global context
        
        t = threading.Thread(target=ListenServers)
        t.start()
    
        socketClients = context.socket(zmq.REP)
        socketClients.bind("tcp://*:8857")

        while True:
            MSJData = socketClients.recv_multipart()

            print("olis")

            Type = Bdecode(MSJData[0])
        
            if Type == "0" :
                Respt = FirstConex()

            elif Type == "1" :
                Respt = UploadFile(Bdecode(MSJData[1]))

            elif Type == "2" :
                print("2")
                
            socketClients.send_multipart(Respt) 



init()
