import time
import zmq
import os
import hashlib


context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:8850")

def TypeUpload(fileName,content):


    fileName = fileName.decode("utf-8")
    fileName = os.path.dirname(os.path.abspath(__file__)) +"/" + fileName
    archivo = open(fileName,'ab')

    archivo.write(content)
    archivo.close()

    socket.send_string("recibido")


def init():

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


init()
