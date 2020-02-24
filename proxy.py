import zmq
CantServUp = 0
ps =  1024*1024*2

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:8857")

def Strencode(strToEncode):
    return str(strToEncode).encode("utf-8")

def FirstConex():
    socket.send_multipart([Strencode(CantServUp),Strencode(ps)])

def UploadFile(FileName):
    socket.send_multipart([b"1",b"localhost",b"9006"])

def init():

        while True:
            MSJData = socket.recv_multipart()

            print("olis")

            Type = MSJData[0]
            Type = Type.decode("utf-8")

            if Type == "0" :
                FirstConex()

            elif Type == "1" :
                UploadFile(MSJData[1].decode("utf-8"))

            elif Type == "2" :
                print("2")

init()
