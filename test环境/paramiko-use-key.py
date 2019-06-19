#!/usr/local/bin/python3
#coding:utf-8 

import paramiko
import sys
import datetime
import os
import re

def help():
    print ("""
\033[33mHelp:

  Welcome to use Felix's python script, this script can help you run commands, send files and get files.
Felix QQ: 279379936
Use this script, you can running for one host or a host group, and you know get file can't for a host group.

Give you examples:

If you want perform command:
    Usage: (for one host) ./paramiko-use-key.py -H [hostip] -c [command]
    Example: ./paramiko-use-key.py -H 10.100.139.245 -c 'ls -al'

    Usage: (for a host group) ./paramiko-use-key.py -F [ip.txt] -c [command]
    Example: ./paramiko-use-key.py -F 'ip.txt' -c 'ls -al'

If you want send file:
    Usage: (for one host) ./paramiko-use-key.py -H [hostip] -s [local_dir] [client_dir] [file]
    Example: ./paramiko-use-key.py -H 10.100.139.245 -s '/opt/Felix' '/tmp' ip.txt

    Usage: (for a host group) ./paramiko-use-key.py -F [ip.txt] -s [local_dir] [client_dir] [file]
    Example: ./paramiko-use-key.py -F ip.txt -s '/opt/Felix' '/tmp' ip.txt

If you want get file:
    Usage: (for one host) ./paramiko-use-key.py -H [hostip] -g [local_dir] [client_dir] [file]
    Example: ./paramiko-use-key.py -H 10.100.139.245 -g '/opt/Felix' '/tmp' ip.txt

ip.txt file content like this:
    1.1.1.1
    2.2.2.2\033[0m    
    """)
    sys.exit()

class SSHConnection(object):

    def __init__(self,host,port,username):
        #self.key = paramiko.RSAKey.from_private_key_file("/app/pythonscript/depthaws.pem")  
        self.key = paramiko.RSAKey.from_private_key_file("/app/jenkins/script/tamcaws-centos-cs.pem")
        #self.key = paramiko.RSAKey.from_private_key_file("/app/jenkins/script/tamcaws-app-cs.pem")  
        self.host = host
        self.port = port
        self.username = username
        self.__k = None

    def connect(self):
        try:
            transport = paramiko.Transport((self.host,self.port))
            transport.connect(username=self.username,pkey=self.key)
            self.__transport = transport
            return 0
        except Exception:
            print ("\033[31mERROR - Connect error! IP: %s!\033[0m" % self.host)
            return 1
            

    def close(self):
        self.__transport.close()

    def cmd(self, command):
        try:
            print ("\033[33mIP:\033[0m", self.host)
            print ("\033[33mPerform command:\033[0m", command)
            print ('\033[32m###########################################################\033[0m')
            ssh = paramiko.SSHClient()
            ssh._transport = self.__transport 
            stdin, stdout, stderr = ssh.exec_command(command)
            result = stdout.read()
            print (result)
            print ('\033[32m###########################################################\033[0m')
            print ('\033[32mScript perform success %s \033[0m' % datetime.datetime.now())
        except Exception:
            print ("\033[31mERROR - Perform error\033[0m")

    def send_file(self,local_dir,client_dir,file_name):
        try:
            print ("\033[33mIP:\033[0m", self.host)
            print ("\033[33mSend file:\033[0m", file_name)
            print ("\033[33mClient_dir:\033[0m", client_dir)
            sftp=paramiko.SFTPClient.from_transport(self.__transport)
            sftp.put(os.path.join(local_dir,file_name),os.path.join(client_dir,file_name))
            print ('\033[32m###########################################################\033[0m')
            print ('\033[32mScript perform success %s \033[0m' % datetime.datetime.now())
        except Exception:
            print ("\033[31mERROR - Perform error\033[0m")
    def get_file(self,local_dir,client_dir,file_name):
        try:
            print ("\033[33mIP:\033[0m", self.host)
            print ("\033[33mget file:\033[0m", file_name)
            print ("\033[33mClient_dir:\033[0m", client_dir)
            sftp=paramiko.SFTPClient.from_transport(self.__transport)
            sftp.get(os.path.join(client_dir,file_name),os.path.join(local_dir,file_name))
            print ('\033[32m###########################################################\033[0m')
            print ('\033[32mScript perform success %s \033[0m' % datetime.datetime.now())
        except Exception:
            print ("\033[31mERROR - Perform error\033[0m")

if __name__ == '__main__':
    #username='ec2-user'
    username='centos'
     #username='app'
    port=22
    if len(sys.argv) > 2:
        if sys.argv[1] == '-H':
            if len(sys.argv) == 5 and sys.argv[3] == '-c':
                hostname=sys.argv[2]
                comm = sys.argv[4]
                # comm
                ssh = SSHConnection(hostname,port,username)
                stat = ssh.connect()
                if stat == 0:
                    ssh.cmd(comm)
                    ssh.close()
            elif len(sys.argv) == 7 and sys.argv[3] == '-s':
                hostname=sys.argv[2]
                local_dir=sys.argv[4]
                client_dir=sys.argv[5]
                file_name=sys.argv[6]
                # send_file
                ssh = SSHConnection(hostname,port,username)
                stat = ssh.connect()
                if stat == 0:
                    ssh.send_file(local_dir,client_dir,file_name)
                    ssh.close()
            elif len(sys.argv) == 7 and sys.argv[3] == '-g':
                hostname=sys.argv[2]
                local_dir=sys.argv[4]
                client_dir=sys.argv[5]
                file_name=sys.argv[6]
                # get_file
                ssh = SSHConnection(hostname,port,username)
                stat = ssh.connect()
                if stat == 0:
                    ssh.get_file(local_dir,client_dir,file_name)
                    ssh.close()
            else:
                help()
        elif sys.argv[1] == '-F':
            ip_file=sys.argv[2]
            file_stat=os.path.exists(ip_file)
            if file_stat:
                f=open(ip_file)
                ips=f.readlines()
                f.close()
                for ip in ips: 
                    ip = ip.strip('\n')
                    if re.match(r'^#', ip):
                        continue
                    if len(sys.argv) == 5 and sys.argv[3] == '-c':
                        hostname = ip
                        comm = sys.argv[4]
                        # comm
                        ssh = SSHConnection(hostname,port,username)
                        stat = ssh.connect()
                        if stat == 0:
                            ssh.cmd(comm)
                            ssh.close()
                    elif len(sys.argv) == 7 and sys.argv[3] == '-s':
                        hostname=ip
                        local_dir=sys.argv[4]
                        client_dir=sys.argv[5]
                        file_name=sys.argv[6]
                        # send_file
                        ssh = SSHConnection(hostname,port,username)
                        stat = ssh.connect()
                        if stat == 0:
                            ssh.send_file(local_dir,client_dir,file_name)
                            ssh.close()
                    else:
                        help()
            else:
                print ("\033[31mERROR - Not found ip_file!\033[0m")
                help()
        else:
            help()
    else:
        help()
