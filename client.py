import socket
import sys
import os.path

if __name__ == "__main__":
    filename = ""
    HOST = 0
    PORT = 0
    # parse command line parameters
    if len (sys.argv) == 4:
        print("\nfile = "+sys.argv[1])
        print("host = "+sys.argv[2])
        print("port = "+sys.argv[3])
        filename = sys.argv[1]
        HOST = sys.argv[2]
        PORT = int(sys.argv[3])
    else:
        print ("You should corretly specify parameters in format:")
        print ("file domain-name|ip-address port-number")
        exit()
        

    total_size = os.path.getsize(filename)
    print("Total size: "+str(total_size)+" bytes\n")
    
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        f = open(filename,'rb')
        filename = filename.encode("utf-8")
        i=1
        l = f.read(1024)
        # add "\x00" after filename
        s.send(filename+b'\x00')
        while (l):
            # print progress
            progress = round(i*1024/total_size*1000)/10
            if(progress>100):
                progress = 100.0
            print ("\rProgress: "+str(progress)+"%", end="")
            i+=1
            s.send(l)
            l = f.read(1024)
        f.close()
        s.shutdown(socket.SHUT_WR)
        server_message = s.recv(1024)
        # get status message from server
        print("\n"+server_message.decode("utf-8"))
        
        
