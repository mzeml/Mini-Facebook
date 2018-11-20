import socket   #for sockets
import sys  #for exit
from check import ip_checksum

# create dgram udp socket
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(3)
except socket.error:
    print 'Failed to create socket'
    sys.exit()

#host = 'localhost';
host = '10.0.0.4'
port = 8888;

seq_no = '0';
accept = True;

while(1) :
    
     if (accept == True):
        msg = raw_input('Enter message to server: ')
        packet = seq_no + ip_checksum(msg) + msg

     try:
        #packet sent
        s.sendto(packet, (host, port))

        #ack recv
        d = s.recvfrom(1024)
        reply = d[0]
        addr = d[1]

        #parse the ack
        ack_seq_no = reply

        while (ack_seq_no != seq_no):
                print 'ERROR: Wrong ack!'
                accept = False;
                continue

        print 'Server reply: ack' + ack_seq_no
        accept = True;

        if (seq_no == '0'):
                seq_no = '1'
        else:
                seq_no = '0'
	#reminder, this changes the CLIENT seq value!

     except socket.timeout:
        print 'ERROR: Timeout, packet resent'
        accept = False;
        continue
