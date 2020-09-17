import socket
import os.path

HOST = ''  
PORT = 15001        

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(10)
while True:
    conn, addr = s.accept()
    print ('Got connection from', addr)
    l = conn.recv(1024)
    f = 0
    name = ""
    ext = ""
    id = 1
    # data is in form "FILENAME\x00FILE"
    # so I get data before "\x00" and use it as filename
    if(l.find(b'\x00')!=-1):    
        filename = l[:l.find(b'\x00')].decode("utf-8") 
        l = l[l.find(b'\x00')+1:]
        if(len(l)==0):
            l = conn.recv(1024)
        id = 1
        if(not os.path.exists(filename)):
            f = open(filename, 'wb')
            name = filename
        else:
            # I parse filename into name+extension to correctly place "_copyN"
            if(filename.find(".")):
               name = filename[:filename.find(".")]
               ext = filename[filename.find("."):]
            else:
                name = filename
            while os.path.exists((name+"_copy%s"+ext) % id):
                id += 1
            filename = name+"_copy"+str(id)+ext
            f = open(filename, 'wb')
        
    else:
        # send message to client if name is more than 1024 byte long
        conn.send(b'Error! Name too long.')
        exit()
    # get data here
    while (l):
        f.write(l)
        l = conn.recv(1024)
    f.close()
    # send message to client
    conn.send(bytes('Success! File created: '+filename, "utf-8"))
    conn.close()
