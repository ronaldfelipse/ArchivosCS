
import zmq
import os
import hashlib

MyIP = ""
MyPort = ""
context = zmq.Context()
socket = context.socket(zmq.REP)
ipProxy = ""
PortProxy = ""

def ip_puerto():
    global MyIP
    MyIP = input("INGRESE LA IP del server\n")
    global MyPort
    MyPort = input("INGRESE PUERTO del server\n")

ip_puerto()

socket.bind("tcp://*:"+MyPort)
PathFile = os.path.dirname(os.path.abspath(__file__))
ServerID = ""

def Strencode(strToEncode):
    return str(strToEncode).encode("utf-8")

def Bdecode(bToEncode):
    return bToEncode.decode("utf-8")

def TypeUpload(fileName,content):

    """
    FolderName = fileName.replace(".",",")

    if (not os.path.exists(PathFile +"/"+FolderName+"/")  ):
        os.mkdir(FolderName)
    """
    fileName =  PathFile +"/"+ fileName + ".rf"
    archivo = open(fileName,'ab')

    archivo.write(content)
    archivo.close()

def ip_puerto():
    global ipProxy
    ipProxy = input("INGRESE LA IP del PROXY\n")
    global PortProxy
    PortProxy = input("INGRESE PUERTO del PROXY\n")
    global ServerID
    ServerID = input("INGRESE EL ID DEL SERVIDOR\n")

def ProxyConect():
    global context
    ip_puerto()
    Path = "tcp://"+ipProxy+":"+PortProxy
    socket = context.socket(zmq.REQ)
    socket.connect(Path)
    socket.send_multipart([b"0",Strencode(MyIP),Strencode(MyPort),Strencode(ServerID)])
    Msjresponse = socket.recv_multipart()
    socket.close()

def TypeDowload(hashID):

    FilePath =  PathFile +"/"+ hashID + ".rf"
    file = open(FilePath, "rb")
    content = file.read()
    MSJ = [b"1",content]
    file.close()
    return MSJ

def init():

    global socket


    ProxyConect()

    while True:

        MSJData = socket.recv_multipart()

        Type = MSJData[0]
        Type = Type.decode("utf-8")

        if Type == "1" :
            TypeUpload(Bdecode(MSJData[1]),MSJData[2])
            hashPart  = hashlib.new("sha1",MSJData[2])
            Respt = [b"1",Strencode(hashPart.hexdigest())]

        elif Type == "2" :
             Respt = TypeDowload(Bdecode(MSJData[1]))


        socket.send_multipart(Respt)


init()
