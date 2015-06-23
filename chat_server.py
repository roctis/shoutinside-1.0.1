#! /usr/bin/python

import socket
import time
import fcntl
import struct
import os
import sys



def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])
    
host =get_ip_address('wlan0')
port = 5000

clients=[]
s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((host, port ))
s.setblocking(0)

terminate_C = False
send_flag=False
print "Server has started the application with ip="+host

while not terminate_C:
    try: 
        data,  addr=s.recvfrom(65536)
        if send_flag:
            print ".", 
            if (data.find('FILE_>T_>STOP')==-1) and (data.find('FILE_TRANSMISSION')==-1):
                f.write(data)
            if data.find('FILE_>T_>STOP')!=-1:
                send_flag=False
                print "Received Completely"
#                print "sending from server",
#                try:
#                    f=open(file,'rb')
#                except:
#                    IOError 
#                l=f.read(1024) 
#            print'.', 
#            if l:
#                s.sendto(l, server)
#            else:
#                send_flag=False
#                print "[TRANSFER COMPLETE]"
#                s.sendto('FILE_>T_>STOP', server)
#        
#                for client in clients:
#                    if client !=a_addr:
#                        s.sendto('FILE_>>TRANSFER', client)
#                        f=open(file,'rb')
#                        l=f.read(1024)
#                        while(l):
#                            print'.', 
#                            s.sendto(l, client)
#                            l=f.read(1024)
#                        s.sendto(str('FILE_>>TRANSFER'), client)
        else:
            if "xbyex" in str(data):
                terminate_C=True
                continue
            if addr not in clients:
                print addr
                clients.append(addr)    
                
            print time.ctime(time.time())+str(addr)+">>"+str(data)
            for client in clients:
                if client !=addr:
                    s.sendto(data,  client)    
            if data.find('FILE_>T_>START')!=-1:
                send_flag=True
                print 'Receiving.', 
                if not os.path.isdir('server_dl/'): os.makedirs('server_dl/')
                file='server_dl/'+data[16:]
                f=open(file, 'wb')
            
        
        
    except:
        pass
    if not send_flag:time.sleep(0.2)
    
s.close
