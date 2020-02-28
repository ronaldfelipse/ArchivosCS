import zmq
import os.path
import hashlib
import json

context = zmq.Context()
ps = 0
ipServer = ""
PortServer = ""
PathFile = os.path.dirname(os.path.abspath(__file__))

def ip_puerto():
    global ipServer
    ipServer = input("INGRESE LA IP del PROXY\n")
    global PortServer
    PortServer = input("INGRESE PUERTO del PROXY\n")

def SendSocketMSJ(IpServer,PortServer,MSJ):
    global context
    Path = "tcp://"+IpServer+":"+PortServer
    socket = context.socket(zmq.REQ)
    socket.connect(Path)
    socket.send_multipart(MSJ)
    Msjresponse = socket.recv_multipart()
    socket.close()
    return Msjresponse



def Strencode(strToEncode):
    return str(strToEncode).encode("utf-8")

def Bdecode(bToEncode):
    return bToEncode.decode("utf-8")

def Upload():

    global ps

    FilePath = input("INGRESE LA RUTA DEL ARCHIVO A SUBIR\n")

    if os.path.isfile(FilePath) :

        file = open(FilePath, "rb")

        file.seek(0, os.SEEK_END)
        size = file.tell()
        NumParts =round ( size / ps )
        if NumParts == 0 :
            NumParts = 1

        FileName = os.path.basename(file.name)
        count = 0
        point = 0
        while True:

            count = count + 1

            file.seek(int(point))
            content = file.read(ps)
            hashPart  = hashlib.new("sha1",content)
            MSJData = SendSocketMSJ(ipServer,PortServer,[b"1",Strencode(FileName),Strencode(count),Strencode(hashPart.hexdigest())])

            if (Bdecode(MSJData[0]) == "1"):

                IPTemp = Bdecode(MSJData[1])
                PortTemp = Bdecode(MSJData[2])

                print("Enviando parte "+str(count)+" de "+ str(NumParts))

                MSJData = SendSocketMSJ(IPTemp,PortTemp,[b"1",Strencode(hashPart.hexdigest()), content])

                if (Bdecode(MSJData[0]) != "1"):
                    print("Error")
                    break
                else:
                    if (Bdecode(MSJData[1]) != hashPart.hexdigest() ) :
                        print("Error integridad archivo")
                        break

                if (point + ps) >= size:
                    break
                else:
                    point = point + ps

            else:
                print("Error")
                break


        file.close()


    else:
        print("El archivo no existe")

def Menu():
    print("Menu \n1.Upload\n2.Download\n3.List")
    return int(input("INGRESE LA OPCIÓN\n"))

def List():
    MSJData = SendSocketMSJ(ipServer,PortServer,[b"2"])

    if (Bdecode(MSJData[0]) == "1"):
        FilesList = Bdecode(MSJData[1])
        print(FilesList)
    else:
        print("Error")

def Download():
    Filename = input("ingrese el nombre del archivo a descargar\n")
    MSJData = SendSocketMSJ(ipServer,PortServer,[b"3",Strencode(Filename)])

    if (Bdecode(MSJData[0]) == "1"):
        FileData = json.loads(Bdecode(MSJData[1]))
        for Part in FileData:
            ServerData = Part["ServerID"].split(":")
            MSJData = SendSocketMSJ(ServerData[0],ServerData[1],[b"2",Strencode(Part["HASH"])])
            if (Bdecode(MSJData[0]) == "1"):

                hashPart  = hashlib.new("sha1",MSJData[1])

                if Part["HASH"] == hashPart.hexdigest():
                    PathFileSave =  PathFile +"/"+ Filename
                    archivo = open(PathFileSave,'ab')
                    archivo.write(MSJData[1])
                    archivo.close()

                else:
                    print("Error integridad archivo")
                    break



            else:
                print("Error")

    else:
        print("Error")



def Init():

        ip_puerto()

        MSJData = SendSocketMSJ(ipServer,PortServer,[b"0"])

        print("Conexion exitosa. "+Bdecode(MSJData[0])+" Servidores online")

        global ps

        ps = int(Bdecode(MSJData[1]))

        while True:

            op = Menu()

            if op == 1 :
                Upload()
            elif op == 2:
                Download()
            elif op == 3:
                List()
            else:
                print("Tipo invalido")


Init()
