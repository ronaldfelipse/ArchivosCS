
import zmq
import os

MyIP = "localhost"
MyPort = "9007"
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:"+MyPort)
PathFile = os.path.dirname(os.path.abspath(__file__))

def Strencode(strToEncode):
    return str(strToEncode).encode("utf-8")

def Bdecode(bToEncode):
    return bToEncode.decode("utf-8")

def TypeUpload(fileName,content):

    fileName = Bdecode(fileName)

    FolderName = fileName.replace(".",",")
    
    if (not os.path.exists(PathFile +"/"+FolderName+"/")  ):
        os.mkdir(FolderName)

    fileName =  PathFile +"/"+FolderName+"/" + fileName
    archivo = open(fileName,'ab')

    archivo.write(content)
    archivo.close()

def ProxyConect():
    global context
    Path = "tcp://localhost:8855"
    socket = context.socket(zmq.REQ)
    socket.connect(Path)
    socket.send_multipart([b"0",Strencode(MyIP),Strencode(MyPort)])
    Msjresponse = socket.recv_multipart()
    socket.close()

def init():
    
    global socket
    
    ProxyConect()

    while True:
        
        MSJData = socket.recv_multipart()

        Type = MSJData[0]
        Type = Type.decode("utf-8")
        
        if Type == "1" :
            TypeUpload(MSJData[1],MSJData[2])

        elif Type == "2" :
            print("2")

        elif Type == "3" :
            print("3")
            
        socket.send_multipart([b"1"])


init()
