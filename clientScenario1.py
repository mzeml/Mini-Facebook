import socket   #for sockets
import sys  #for exit
import getpass

# UDP Socket
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
    #s.settimeout(3)
except socket.error:
    print 'Failed to create socket'
    sys.exit()

#host = 'localhost';
host = '10.0.0.4'
port = 8888;

#id_flag = '0'
tempPacket = '0' + 'INIT'

#FIXME: Send an intial packet to ask server what I need (server will respond you need to login )
s.sendto(tempPacket, (host, port))

while(1) :
  #FIXME: Change this to be in an if statment for when user has already logged in. Inital packet should be a "handskake packet"
  #msg = raw_input('Enter message to server: ')
  #packet = id_flag + msg

  #packet sent
  #s.sendto(packet, (host, port))
  d = s.recvfrom(1024)
  reply = d[0]
  #FIXME: parse for ID flag and have if statements for each ID flag (eg 1 means enter user!)
  addr = d[1]
  
  flag_id = reply[0]
  
  #have a check were if we get an error flag, we send a flag asking for last packet
  
  if '1' == flag_id:
    msg = raw_input('Enter your username: ')
    id_flag = '2'
    packet = id_flag + msg
    s.sendto(packet, (host, port)) 
    
  elif '3' == flag_id:
    msg = getpass.getpass()
    id_flag = '4'
    packet = id_flag + msg
    s.sendto(packet, (host, port)) 
  #elif statement if -2 or -3, re enter user and pw (set flag back)
  elif '5' == flag_id:
    print 'Main Menu: Select an option below by typing the number'
    print 'Logout [1]'
    print 'Change password [2]'
    #print 'Send message to a user [3]'
    menuChoice = raw_input('Select an option: ')
    if menuChoice == '1':
      id_flag = '6'
    elif menuChoice == '2':
      id_flag = '' #FIXME
    else:
      id_flag = '-1'
    msg = 'MENU'
    packet = id_flag + msg
    s.sendto(packet, (host, port)) 
    
    #id_flag = ''
  elif '7' == flag_id:
    #we logged out
    print 'Log out successful! Goodbye!'
    exit
    #break
    sys.exit()
    
    
  else:
    print 'ERROR, FLAGID: ' + flag_id
    break
    
    
    
    
    