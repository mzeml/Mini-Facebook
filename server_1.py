import socket
import sys
from check import ip_checksum
 
HOST = '10.0.0.4'   # Symbolic name meaning all available interfaces
PORT = 8888 # Arbitrary non-privileged port
 
# Datagram (udp) socket
try :
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print 'Socket created'
except socket.error, msg :
    print 'Failed to create socket. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()
 
 
# Bind socket to local host and port
try:
    s.bind((HOST, PORT))
except socket.error , msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()
     
print 'Socket bind complete'


#cur_seq_no = '0' #not needed as an array keeps track of seq #'s
seq_no_arr = []
client_addr_arr = []
 
#now keep talking with the client
while 1:
    # receive data from client (data, addr)
    d = s.recvfrom(1024)
    data = d[0]
    addr = d[1]
    if (addr[0] not in client_addr_arr): #adds the client's addr to array if they haven't connected already
	client_addr_arr.append(addr[0])
	seq_no_arr.append('0') #the index for this value corresponds to the above array 
	 
    seq_index = client_addr_arr.index(addr[0])

    #parses the packet which contains seq number, the checksum, and the actual message
    seq_no = data[0:1]
    checksum = data[1:3]
    msg = data[3:]
    
    #if we have no data, we're done here 
    if not data: 
        break

    #if the recv checksum value fails the check, packet is corrupt
    if (ip_checksum(msg) != checksum):
        print 'ERROR: Packet is corrupt!'
	continue

    #Checks to see if we recv a packet out of sequence    
    if (seq_no != seq_no_arr[seqq_index]):
	print 'ERROR: Wrong seq_no!'
	continue
    
    #send the corresponding ack saying we got the packet 
    s.sendto(seq_no, addr)

    print 'Server recv this from client: ' + msg
   
    #sets the new seq value
    if (seq_no_arr[seq_index] == '0'):
	seq_no_arr[seq_index] = '1'
    else:
	seq_no_arr[seq_index] = '0'
     
s.close() 
