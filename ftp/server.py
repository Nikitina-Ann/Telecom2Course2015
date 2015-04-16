__author__ = 'Аня'
import socket
import threading
import os
import time
import random
class User :
    def __init__(self,user_id):
        self.dir=""
        self.user_id=user_id
        self.type="binary"
        self.name=""
        self.password=""
    def authUser(self,login,password):
        self.name=login
        self.password=password
class Server:
    def __init__(self,directory):
        self.users={}
        self.activeUsers=[]
        self.readFileUsers()
        self.directory=directory
        f = open('protocol.txt', 'w')
        f.write("id_______логин_______комманда____количество клиентов\r\n")
        f.close
    def writeProtocolFile(self,command,User):
        f = open('protocol.txt', 'a')
        f.write("%f______%s______%s______%d\r\n" %(User.user_id,User.name,command,len(self.activeUsers)))
        f.close
    def readFileUsers(self):
        try:
            f = open('user.txt', 'r')
            n=f.readlines()
            for i in n:
                i=i[0:len(i)-1]
                i=i.split(',')
                self.users[i[0]]=i[1]
            f.close
            return True
        except IOError:
            return False
    def hasUser(self,login,password):
        if(self.users.get(login)==password):
            return True
        elif(login=='anonymous'):
            return True
        else:
            return False
    def deleteFile(self,pathFile,userDir):
        pathFile=self.setPath(pathFile,userDir)
        try:
            os.remove(pathFile)
            return True
        except FileNotFoundError:
            return False
    def deleteDir(self,pathFile,userDir):
        pathDir=self.setPath(pathFile,userDir)
        try:
            for top, dirs, files in os.walk(pathDir):
                for nm in files:
                    os.remove(os.path.join(top, nm))
            for i in os.listdir(pathDir):
                self.deleteDir(pathFile+"\\"+i,userDir)
            os.rmdir(pathDir)
            return True
        except Exception:
            return False
    def mkDir(self,pathFile,userDir):
        pathDir=self.setPath(pathFile,userDir)
        try:
            os.makedirs(pathDir)
            return True
        except Exception:
            return False
    def setPath(self,pathFile,userDir):
        if(pathFile[0]=="\\"):
            pathFile=self.directory+pathFile
        elif(len(userDir)!=0):
            pathFile=self.directory+"\\"+userDir+"\\"+pathFile
        else:
            pathFile=self.directory+"\\"+pathFile
        return pathFile
    def deleteUser(self,user_id):
        for i in self.activeUsers:
            if(i.user_id==user_id):
                self.activeUsers.remove(i)
                self.writeProtocolFile("отключение",i)
    def auth(self,login,password,user_id):
        for i in self.activeUsers:
            if(i.user_id==user_id):
                i.authUser(login,password)
    def newUser(self,user_id):
        newUser=User(user_id)
        self.activeUsers.append(newUser)
        self.writeProtocolFile("подключение",newUser)
    def setType(self,user_id,type):
        for i in self.activeUsers:
            if(i.user_id==user_id):
                if(type=="I"):
                    i.type="binary"
                else:
                    i.type="asci"
            return True
        return False
    def serverList(self,flag,userDir):
        data=""
        path=server.directory+"\\"+userDir
        files = os.listdir(path)
        for i in files:
            if(flag==False):
                data=data+i+"\n"
            else:
                data=data+self.serverNlst(path,i)+"\n"
        return data
    def serverNlst(self,path,i):
        pathFile=path+"\\"+i
        metadata=os.stat(pathFile)
        timeFile=time.localtime(metadata.st_ctime)
        cttime='%d.%d.%d' %(timeFile.tm_mday,timeFile.tm_mon,timeFile.tm_year)
        timeFile=time.localtime(metadata.st_mtime)
        mttime='%d.%d.%d' %(timeFile.tm_mday,timeFile.tm_mon,timeFile.tm_year)
        data='%s    %s    %s    %d' % (pathFile,cttime,mttime,metadata.st_size)
        return data
    def serverSetDir(self,dir,userDir):
        if(dir[0]=="\\"):
            currDir=self.directory+dir
        else:
            currDir=self.directory+"\\"+userDir+"\\"+dir
        try:
            os.listdir(currDir)
            return True
        except FileNotFoundError:
            return False

class SocketThread(threading.Thread):
    def __init__(self, conn, addr):
        self.conn = conn
        self.addr =addr
        threading.Thread.__init__(self)
        self.port=False
        self.id=False
    def run ( self ):
        global thread
        global server
        thread = thread + 1
        user_id=random.random()
        self.user=User(user_id)
        server.newUser(user_id)
        self.conn.send(b"220 Welcome to FTP-Server\r\n")
        login = self.conn.recv(size)
        login=login[5:len(login)-2].decode("utf-8")
        self.auth(login)
        while(1):
            command = self.conn.recv(size)
            command=command[0:len(command)-2].decode("utf-8")
            command=command.split(" ")
            print(command)
            server.writeProtocolFile(command,self.user)
            if(command[0]=='QUIT'):
                server.deleteUser(self.user.user_id)
                self.conn.send(b'221 Goodbye.\r\n')
                break
            elif(command[0]=='USER'):
                login=command[1]
                self.auth(login)
            elif(command[0]=='XPWD'):
                self.pwd()
            elif(command[0]=='CWD'):
                dir=command[1]
                if(dir==".."):
                    self.cwdUp()
                else:
                    self.cwd(dir)
            elif(command[0]=='PORT'):
                path=command[1]
                self.comPort(path)
            elif(command[0]=='NLST'):
                self.list(False)
            elif(command[0]=='LIST'):
                self.list(True)
            elif(command[0]=='DELE'):
                path=command[1]
                self.delete(path)
            elif(command[0]=='XRMD'):
                path=command[1]
                self.deleteDir(path)
            elif(command[0]=='TYPE'):
                type=command[1]
                self.setType(type)
            elif(command[0]=='XMKD'):
                path=command[1]
                self.mkDir(path)
            elif(command[0]=='RETR'):
                file=command[1]
                self.comRetr(file)
            elif(command[0]=='STOR'):
                file=command[1]
                self.comStor(file)
        thread=thread-1
        self.conn.close()
    def setType(self,type):
        if(server.setType(self.user.user_id,type)):
            if(type=="I"):
                self.user.type="binary"
            else:
                self.user.type="asci"
            self.conn.send(b'200 Type set to ' + type.encode("utf-8")+b'\r\n')
        else:
            self.conn.send(b'502 Command not implemented\r\n')
    def mkDir(self,path):
        if(self.id==True):
             if(server.mkDir(path,self.user.dir)):
                self.conn.send(b'257 Directory '+path.encode("utf-8")+b' create\r\n')
             else:
                 self.conn.send(b'550 Directory '+path.encode("utf-8")+b' not create\r\n')
        else:
            self.conn.send(b'530 Please login with USER and PASS\r\n')

    def deleteDir(self,path):
        if(self.id==True):
            if(server.deleteDir(path,self.user.dir)):
                self.conn.send(b'250 Directory '+path.encode("utf-8")+b' deleted\r\n')
            else:
                self.conn.send(b'550 Directory '+path.encode("utf-8")+b' not found\r\n')
        else:
            self.conn.send(b'530 Please login with USER and PASS\r\n')
    def delete(self,path):
        if(self.id==True):
            if(server.deleteFile(path,self.user.dir)):
                self.conn.send(b'250 File '+path.encode("utf-8")+b' deleted\r\n')
            else:
                self.conn.send(b'550 File '+path.encode("utf-8")+b' not found\r\n')
        else:
            self.conn.send(b'530 Please login with USER and PASS\r\n')

    def list(self,flag):
        if(self.port==True):
            self.conn.send(b'150 Accepted data connection\r\n')
            try:
                data=server.serverList(flag,self.user.dir)
                self.clientSock.send(data.encode("utf-8")+b'\r\n')
                self.clientSock.close()
                self.conn.send(b'226 Transfer complete\r\n')
            except FileNotFoundError:
                self.conn.send(b'500 File not found\r\n')
        else:
            self.conn.send(b'425 Unable to build data connection: Connection refused\r\n')
    def comPort(self,path):
        if(self.id==True):
            path=path.split(",")
            try:
                address=path[0]+'.'+path[1]+'.'+path[2]+'.'+path[3]
                port=int(path[4])*256+int(path[5])
                self.clientSock=socket.socket()
                self.clientSock.connect((address, port))
                self.port=True
                self.conn.send(b'200 PORT command succesful\r\n')
            except Exception:
                print("Error format of command PORT")
                self.conn.send(b'500 Illegal PORT command\r\n')
        else:
            self.conn.send(b'530 Please login with USER and PASS\r\n')
    def cwdUp(self):
        if(self.id==True):
            list=self.user.dir.split("\\")
            list=list[:len(list)-1]
            self.user.dir=""
            for i in list:
                self.user.dir=self.user.dir+i
                if(i!=list[len(list)-1]):
                    self.user.dir=self.user.dir+"\\"
            self.conn.send(b'250 Current directory is \\'+self.user.dir.encode("utf-8")+b'\r\n')
        else:
            self.conn.send(b'530 Please login with USER and PASS\r\n')
    def cwd(self,dir):
        if(self.id==True):
            if(server.serverSetDir(dir,self.user.dir)==True):
                if(dir[0]=="\\"):
                    self.user.dir=dir[1:]
                elif(len(self.user.dir)==0):
                    self.user.dir=dir
                else:
                    self.user.dir=self.user.dir+"\\"+dir
                self.conn.send(b'250 Current directory is \\'+self.user.dir.encode("utf-8")+b'\r\n')
            else:
                self.conn.send(b'502 Command not implemented\r\n')
        else:
            self.conn.send(b'530 Please login with USER and PASS\r\n')
    def pwd(self):
        if(self.id==True):
            direct='\\"%s" is the current directory\r\n' % self.user.dir
            self.conn.send(direct.encode("utf-8"))
        else:
            self.conn.send(b'530 Please login with USER and PASS\r\n')
    def auth(self,login):
        if(self.id==False):
            self.conn.send(b'331 Write the password\r\n')
            password = self.conn.recv(size)
            password=password[5:len(password)-2].decode("utf-8")
            if(server.hasUser(login,password)==False):
                self.conn.send(b'530 Login incorrect\r\n')
            else:
                self.conn.send(b'230 User '+ login.encode("utf-8")+ b' logged in\r\n')
                server.auth(login,password,self.user.user_id)
                self.user.authUser(login,password)
                self.id=True
        else:
            self.conn.send(b'You are already logged in\r\n')
    def retrFileBinary(self,path):
        f=open(path,"rb")
        self.conn.send(b'150 Accepted data connection\r\n')
        while True:
            data = f.read(1024)
            if not data: break
            self.clientSock.send(data)
        f.close()
    def retrFileAscii(self,path):
        try:
            f=open(path,"r")
            data = f.read(1024)
            self.conn.send(b'150 Accepted data connection\r\n')
            while True:
                if not data: break
                self.clientSock.send((data).encode("latin1"))
                data = f.read(1024)
            f.close()
            return True
        except Exception:
            return False

    def comRetr(self,file):
        path=server.setPath(file,self.user.dir)
        if(self.port==True):
            try:
                if(self.user.type=="binary"):
                    self.retrFileBinary(path)
                elif(self.retrFileAscii(path)==False):
                    self.conn.send(b'406 TYPE must binary\r\n')
                self.conn.send(b'226 Transfer complete\r\n')
                self.clientSock.close()
            except Exception:
                self.conn.send(b'500 File not found\r\n')
        else:
            self.conn.send(b'425 Unable to build data connection: Connection refused\r\n')
    def comStor(self,file):
        path=server.setPath(file,self.user.dir)
        if(self.port==True):
            if(self.user.type=="binary"):
                self.storeFileBinary(path)
            elif(self.storeFileAscii(path)==False):
                self.conn.send(b'406 TYPE must binary\r\n')
            self.conn.send(b'226 Transfer complete\r\n')
            self.clientSock.close()
        else:
            self.conn.send(b'425 Unable to build data connection: Connection refused\r\n')

    def storeFileBinary(self,path):
        f=open(path,"wb")
        self.conn.send(b'150 Accepted data connection\r\n')
        while True:
            data=self.clientSock.recv(size)
            if not data: break
            f.write(data)
        f.close()
    def storeFileAscii(self,path):
        try:
            f=open(path,"wt")
            self.conn.send(b'150 Accepted data connection\r\n')
            data = self.clientSock.recv(size)
            while True:
                if not data: break
                f.write(data.decode("utf-8"))
                data = self.clientSock.recv(size)
            f.close()
            return True
        except Exception:
            f.close()
            os.remove(path)
            return False


size=1024
thread=0
server=Server('D:\\projects')
b = True
sock = socket.socket()
sock.bind(('localhost', 21))
sock.listen(5)
while 1:
    conn, addr = sock.accept()
    SocketThread(conn, addr).start()
