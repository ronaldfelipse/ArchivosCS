import zmq
import os.path

context = zmq.Context()
ps = 0
ipServer = ""
PortServer = ""

def ip_puerto():
    global ipServer 
    ipServer = input("INGRESE LA IP del server\n")
    ipServer = "localhost"
    global PortServer 
    PortServer = input("INGRESE PUERTO del server\n")
    PortServer = "8857"

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

    FilePath = "/Users/Ronald/Downloads/Macaco.mp4"

    if os.path.isfile(FilePath) :

        file = open(FilePath, "rb")

        file.seek(0, os.SEEK_END)
        size = file.tell()
        NumParts =round ( size / ps )
     
        FileName = os.path.basename(file.name)
        count = 0
        point = 0
        while True:

            file.seek(int(point))
            content = file.read(ps)

            MSJData = SendSocketMSJ(ipServer,PortServer,[b"1",Strencode(FileName)])

            if (Bdecode(MSJData[0]) == "1"):
                
                IPTemp = Bdecode(MSJData[1])
                PortTemp = Bdecode(MSJData[2])
                count = count + 1
                print("Enviando parte "+str(count)+" de "+ str(NumParts))

                MSJData = SendSocketMSJ(IPTemp,PortTemp,[b"1",Strencode(FileName), content])
                
                
                if (Bdecode(MSJData[0]) != "1"):
                    print("Error")
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
