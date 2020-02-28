import zmq
import threading
import json
import os.path
import copy

ps = 100 # 1024*1024*2
Servers = []
FilesList = {}
PathData = os.path.dirname(os.path.abspath(__file__))
PortServers = ""
ClientServers = ""

context = zmq.Context()

ServerPointer = 0

def Bdecode(bToEncode):
    return bToEncode.decode("utf-8")

def Strencode(strToEncode):
    return str(strToEncode).encode("utf-8")

def FirstConex():
    return ([Strencode(len(Servers)),Strencode(ps)])

def UploadFile(FileName,NumbePart,hash):

    global FilesList
    global Servers
    global ServerPointer

    DataServer = Servers[ServerPointer].split(":")

    if NumbePart == "1":
        FilesList[FileName] = []

    FilesList[FileName].append({
    'NumberPart': NumbePart,
    'ServerID': DataServer[2],
    'HASH': hash})

    if ( (ServerPointer+1) == len(Servers) ):
            ServerPointer = 0
    else:
        ServerPointer = ServerPointer + 1

    return ([b"1",Strencode(DataServer[0]),Strencode(DataServer[1]) ] )

def NewServerON(Direccion,Puerto,ServerID):

        global Servers
        Servers.append(Direccion+":"+Puerto+":"+ServerID)


def ListenServers():

        global context
        global PortServers

        socketServers = context.socket(zmq.REP)
        socketServers.bind("tcp://*:"+PortServers)

        while True:
            MSJData = socketServers.recv_multipart()

            Type = Bdecode(MSJData[0])

            if Type == "0" :
                 NewServerON(Bdecode(MSJData[1]),Bdecode(MSJData[2]),Bdecode(MSJData[3]))
                 print("NewServerON")

            socketServers.send_multipart([b"1"])

def LoadFilesList():

    global FilesList

    if os.path.isfile(PathData+"/data.json") :
        with open('data.json') as file:
            FilesList = json.load(file)



def SaveFilesList():
    global FilesList
    with open('data.json', 'w') as file:
        json.dump(FilesList, file, indent=4)

def GetListFiles():

    ListF = ""
    for File in FilesList:
        if ListF != "":
            ListF = ListF+"|"
        ListF = ListF + File
    return [b"1",Strencode(ListF)]

def GetDataServerXId(ServerID):
    global Servers
    for Server in Servers:
        DataServer = Server.split(":")
        if DataServer[2] == str(ServerID) :
            return DataServer[0]+":"+DataServer[1]
    return 0


def DowloadFile(FileName):

    global FilesList

    if FileName in FilesList:
        Partes = copy.deepcopy(FilesList[FileName])
        for i in range(len(Partes)):
            SvID = GetDataServerXId(Partes[int(i)]["ServerID"])
            if str(SvID) == "0" :
                return [b"0",b"No se encontro activo el servidor de una de las partes"]
            Partes[i]["ServerID"] = SvID

        result = json.dumps(Partes)
        return [b"1",Strencode(result)]

    else:
        return [b"0",b"Error el archivo solicitado no existe"]


def init():

        global context

        global ClientServers
        global PortServers

        ClientServers = input("INGRESE PUERTO PARA LOS CLIENTES\n")
        PortServers = input("INGRESE PUERTO PARA LOS SERVERS\n")

        LoadFilesList()

        t = threading.Thread(target=ListenServers)
        t.start()

        socketClients = context.socket(zmq.REP)
        socketClients.bind("tcp://*:"+ClientServers)

        while True:
            MSJData = socketClients.recv_multipart()

            Type = Bdecode(MSJData[0])

            if Type == "0" :
                Respt = FirstConex()

            elif Type == "1" :
                Respt = UploadFile(Bdecode(MSJData[1]),Bdecode(MSJData[2]),Bdecode(MSJData[3]))
                SaveFilesList()

            elif Type == "2" :
                Respt = GetListFiles()

            elif Type == "3" :
                Respt = DowloadFile(Bdecode(MSJData[1]))

            socketClients.send_multipart(Respt)

init()
