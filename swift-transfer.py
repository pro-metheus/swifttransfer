## file/folder transfer script

##app config ##

import os,socket

ip='127.0.0.1'

port=8000


size=10000000 #10mb

#code 1 sending folder name
#code 2 sending file

#############




def get_name(path):
    name=[]
    for ch in path:
        if ch=='/':
            name=[]
        else:
            name.append(ch)
    return ''.join(name)

def sender():
    loc=input("enter abs location of folder to send")
    name=get_name(loc)
    
    client.send(name.encode())  #server send the name of folder, recreate it
    cont=os.listdir(loc)
    for c in cont:
        client.send('1'.encode())
        client.send(c.encode())  #server sends the first file name
        f=open(loc+'/'+c,'rb')
        chunk=f.read(size)
        while(chunk):
            #client.send(2.encode())
            client.send(chunk)
            chunk=f.read(size)
            print(c+' created...')
    client.send('0'.encode())


def reciever(root):
    d=client.recv(1024).decode()   #name of the main folder to create
    os.mkdir(d)
    os.chdir(root+'/'+d)
    p=client.recv(1024).decode()
    if p=='0':
        return 0
    elif p=='1':
        fname=client.recv(1024).decode()
    f=open(root+'/'+d+'/'+fname,'wb')
    cont=client.recv(size)
    while(cont):
        f.write(cont)
        cont=client.recv(size)



if __name__=='__main__':
    print("1 for sending, 2 for recieving")
    op=int(input())
    if op==1:
        server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        server.bind((ip,port))
        server.listen(2)
        (client,add)=server.accept()
        sender()
    if op==2:
        root=input('enter abs location to store to')
        client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        client.connect((ip,port))
        reciever(root)
        
    
