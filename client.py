#!/usr/bin/python          
class TCP_connection_CLIENT:
    'class for connection oriented connected for file transfer'
    tcp_conn_count=0
    
    def __init__(self, (host_port), buffer_size):
        self.host_port=host_port
        self.buffer_size=buffer_size
        #create tcp socket and binding'
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect(self.host_port)
        TCP_connection_CLIENT.tcp_conn_count+=1
        
    def connection_establish(self):
        self.s.connect(self.host_port)
        
    def receive_file(self, filename):
        #client,addr = self.s.accept()
        try:
            f=file(filename,'wb')
        except:
            print "UNABLE TO WRITE FILE"
            pass
        data = str(self.s.recv(1024))
        while (data.find("@!fxixlxexT5tx2rxExnxd@!")):
            f.write(data)
            data=str(self.s.recv(1024))
            
        f.close()
        #client.close()
        print "Received File: %s" % (filename)
        
    def send_file(self, filename):
        try:
            f=open(filename, 'rb')
        except: 
            print "UNABLE TO READ THE FILE"
            pass
        data=f.read(1024)
        print "\nSending "+filename+"......................................", 
        while data:
            self.s.send(data)
            data=f.read(1024)
            
        self.s.send('@!fxixlxexT5tx2rxExnxd@!')
        print "[100%]\n[SENDING COMPLETED]\n"
        #self.s.close()
        
    def close_socket(self):
        self.s.close()
    

class UDP_connection_CLIENT:
        'Class for connection less connection for message transfer'
        udp_conn_count=0
        def __init__(self, (host_port), buffer_size):
            self.server=host_port
            self.buffer_size=buffer_size
            self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            UDP_connection_CLIENT.udp_conn_count+=1
            
        def receive_message(self):
            'receive udp message'
            self.data,self.addr = self.s.recvfrom(self.buffer_size)
            self.data=str(self.data)
            return (self.data, self.addr)
            
        def send_message(self, data):
            'receive udp message'
            self.s.sendto(data, self.server)
            
        def display_message(self):
            print "\n"+self.data
            
        def close_socket(self):
            self.s.close()
    
            

#FLAGS
save_flag = False
shutdown=False
file_tansfer=False

#FUNCTIONS

#CHECK_OPTIONS

def check_option_for_saving(option):
    #saving to file
    global save_flag
    global alias
    if option.find('>save<')!=-1:
        if not save_flag:
            print "SAVING \'data/"+alias+"txt\'" 
        else:
            print "COMPLETED...............................................[100%]\n"
        save_flag=not save_flag
        
    if save_flag:
        save_to_file(alias, option)
    
    #saving completed
    

#SAVING FUNCTION
def save_to_file(filename, data):
    path='data/'+filename+'.txt'
    if not os.path.isdir('data'): os.makedirs('data')
    f=open(path, 'a')
    f.write(data)
    f.write('\n')
    f.close()

def get_filename(path):
    path.split
    filename=path.rsplit('/', 1)
    filename=filename[-1]
    return filename
        
def get_filename_from_text(data):
    fname=data.split('#')
    return fname[1]
    
def get_client_temp_path(fname, dir):
    if not os.path.isdir(dir): os.makedirs(dir)
    fname=dir+fname
    return fname

#RECEIVING FUNCTION

def receving_message(name, text,  doc):
    global filename
    global shutdown
    global save_flag
    global alias
    while not shutdown:
        try:
            tLock.acquire()
            while True:
                msg=text.receive_message()
                if msg[0].find('@!file@!')!=-1:
                    file_name=get_filename_from_text(msg[0])
                    file_name=get_client_temp_path(file_name, 'downloaded/')
                    doc.receive_file(file_name)
                else:
                    text.display_message()
                if save_flag:save_to_file(alias, msg[0])
                
        except:
            pass
        finally:
            tLock.release()
            
        time.sleep(0.2)


        
    
#MAIN FUNCTION STARTS HERE#
if __name__ == '__main__':
    import sys
    import getopt
    import os
    import socket
    import time
    import threading
    print
    print 'USAGE:client.py [server_ipaddress]'
    print 'press >save< to save the conversation'
    print "press >file< to send the file to all the members"
    print "press >fileto< to send the file to a specific ip"
    print
    print
    
    args, sources = getopt.getopt(sys.argv[1:], 'f:', 'shotdir=')
    args = dict(args)
    if len(sources)==0:host='127.0.0.1'
    else:host=sources[0]

    #global variables
    HOST =host
    PORT = 5000
    host_port=(HOST, PORT)
    buffer_size=8000
    
    
    
    #program
#    path=raw_input("\nEnter the path of file:\n ")
#    filename=get_filename(path)
#    TCP_connection_CLIENT(host_port, buffer_size).tcp_send_file(path)
#   
    tLock = threading.Lock()
    text=UDP_connection_CLIENT(host_port, buffer_size)
    doc= TCP_connection_CLIENT(host_port, buffer_size)
    rT = threading.Thread(target=receving_message, args=("receive_msg",text, doc))
    rT.start()
    alias=str(raw_input("\nName: "))
 
    while not shutdown:
        msg=str(raw_input("[self] "))
        if msg=='>bye<':
            shutdown=True
        #saving to file
        elif msg=='>save<': save_flag=not save_flag
        elif save_flag:
            save_to_file(alias, msg)
        #saving completed
        #sendig file
        elif msg.find('>file<')!=-1:
            #file_transfer=True
            path=str(raw_input("\nEnter the path of file e.g: 'data/foo.txt'  :\n"))
            filename=get_filename(path)
            text.send_message('@!file@!'+'#'+filename)
            doc.send_file(path)
        elif msg.find('>fileto<')!=-1:
            file_transfer=True
            path=str(raw_input("\nEnter the path of file e.g: 'data/foo.txt'  :\n"))
            filename=get_filename(path)
            address=str(raw_input("\nEnter the ip address of destination e.g: 192.168.0.34  :\n"))
            path_ip=str('@!fileto@!'+'#'+filename+"#"+address.strip())
            text.send_message(path_ip)
        #sendig file ends here
        else:
            msg=alias+':'+msg
            text.send_message(msg)
        time.sleep(0.2)
    rT.join()    
    text.close_socket()
    
