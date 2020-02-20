import zmq
import math
import sys
import os.path
import time

ps =  45 #1024*1024*2

context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:8850")
Parmameters  = sys.argv

def Upload():

    FilePath = Parmameters[2]
    if os.path.isfile(FilePath) :

        file = open(FilePath, "rb")

        file.seek(0, os.SEEK_END)
        size = file.tell()

        FileName = os.path.basename(file.name)
        
        point = 0
        while True:

            file.seek(int(point))
            content = file.read(ps)

            socket.send_multipart([b"1",FileName.encode("utf-8"), content])
            respt = socket.recv()

            if (point + ps) >= size:
                break
            else:

                point = point + ps


        file.close()


    else:
        print("El archivo no existe")



def Init():

    Type = Parmameters[1]

    if Type.upper() == "UPLOAD":
        Upload()

    elif Type.upper() == "DOWLOAD":
        socket.send_multipart([b"2"])

    elif Type.upper() == "LIST":
        socket.send_multipart([b"3"])

    else:
        print("Tipo invalido")


Init()
