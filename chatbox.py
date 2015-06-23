if __name__ == '__main__':
    import sys
    import getopt
    import os
    print 'USAGE:chatbox.py [<server_ipaddress>]'
    print 'press -s to save the conversation'
    print "press -f to send the file"
    save_flag=False
    send_flag=False
    args, sources = getopt.getopt(sys.argv[1:], 'f:', 'shotdir=')
    args = dict(args)
    if len(sources)==0:host='127.0.0.1'
    else:host=sources[0]
    port=0
    
    def save_to_file(filename, data):
        mpath='data/'
        path='data/'+filename+'.txt'
        if not os.path.isdir(mpath): os.makedirs(mpath)
        fo=open(path, 'a')
        fo.write(data)
        fo.write('\n')
        fo.close()

    import time
    import socket
    import threading
    
    tLock = threading.Lock()
    shutdown = False
    terminate_C = False
    
    def receving(name, sock):
        while not terminate_C:
            try:
                tLock.acquire()
                while True:
                    data, addr = sock.recvfrom(1024)
                    global save_flag
                    global send_flag
                    if save_flag==True:save_to_file(name, data)
                    if data.find('FILE_>>TRANSFER')!=-1:send_flag=not send_flag
                    if send_flag:
                        print 'Receiving file.', 
                        if not os.path.isdir('Downloads/'): os.makedirs('Downloads/')
                        f=open('Downloads/'+name+str(time.ctime(time.time())), 'wb')
                        l,  a_addr=sock.recvfrom(1024)
                        while(l):
                            f.write(l)
                            l,  a_addr=sock.recvfrom(1024)
                            print '.', 
                        
                        print '[Transfer Complete]'
                    else:
                            print data
                    time.sleep(0.2)
            except:
                pass
            finally:
                tLock.release()
            time.sleep(0.2)    
                
    
    server = (host,5000)
    
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    #s.bind((host, port))
    s.setblocking(0)
    
    alias = raw_input("Name: ")
        
    rT = threading.Thread(target=receving, args=(alias,s))
    rT.start()
        
    message = raw_input("")
    while not terminate_C :
        if message =='byebye':
            terminate_C = True
            
        
        if message.find(str('-s'))!=-1:save_flag = not save_flag
        
        if save_flag==True:save_to_file(alias, message)
        
        
        
        if message.find(str('--file'))!=-1:
            print "Sending.", 
            send_flag=True
            file=message[message.find('[')+1:message.find(']')] 
            filename=file.rsplit('/', 1)
            filename=filename[-1]
            message=str(filename)
            s.sendto(str('FILE_>T_>START_>')+message, server)
            try:
                f=open(file,'rb')
            except:
                pass
            
        
        if send_flag:
            print'.', 
            l=f.read(1024) 
            if len(l):
                s.sendto(l, server)
            else:
                send_flag=False
                print "[TRANSFER COMPLETE]"
                s.sendto('FILE_>T_>STOP', server)
            
        else: 
            if message != ' ':
            	s.sendto(alias + ": " + message, server)
            message = raw_input("")
        #tLock.release()
        time.sleep(0.2)
    
    shudown = True
    rT.join()
    s.close()
    exit()
