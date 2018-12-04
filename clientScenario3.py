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
tempPacket = '00' + 'INIT'

#Send an intial packet to ask server what I need (server will respond you need to login )
s.sendto(tempPacket, (host, port))

while(1) :
  d = s.recvfrom(1024)
  reply = d[0]
  addr = d[1]
  menuChoice = ''
  
  flag_id = reply[:2]
  #print flag_id

  #have a check were if we get an error flag, we send a flag asking for last packet

  #server sees us, asked for userName
  if '01' == flag_id:
    msg = raw_input('Enter your username: ')
    id_flag = '02'
    packet = id_flag + msg
    s.sendto(packet, (host, port)) 

  elif '03' == flag_id or '09' == flag_id:
    msg = getpass.getpass()
    if '03' == flag_id:
      id_flag = '04'
    else:
      id_flag = 'KK'
    packet = id_flag + msg
    s.sendto(packet, (host, port)) 
  #elif statement if -2 or -3, re enter user and pw (set flag back)
  elif '05' == flag_id or flag_id == '15': #or add another flag indicating that unread messages exist
    print '\n'
    if '05' == flag_id:
      print 'You have 0 unread messages \n'
    elif '15' == flag_id:
      print 'DEBUG: FLAG !5, ENTERING MENU..... \n' #FIXME, remove this
      
    #else 
      #print unread count 
    print 'Main Menu: Select an option below by typing the number'
    print 'Logout [1]'
    print 'Change password [2]'
    print 'Send message to a user [3]'
    print 'Send message to all online [4]'
    print 'Read unread messages [5]'

    menuChoice = raw_input('Select an option: ')

    if menuChoice == '1':
      id_flag = '06'
      msg = 'MENU'
      packet = id_flag + msg
      s.sendto(packet, (host, port)) 
    elif menuChoice == '2':
      id_flag = '08'
      msg = 'MENU'
      packet = id_flag + msg
      s.sendto(packet, (host, port)) 
    elif menuChoice == '3':
      #ask who to send it to. Server will respond with a flag "X" if person is a valid user. Else, flag Y tells client not valid, try again
      msg = raw_input('Enter the username of who you want to send the message to: ')
      id_flag = 'UN'
      #print 'Message to server ' + msg
      packet = id_flag + msg
      s.sendto(packet, (host, port))
      #break
    #elif menuChoice == '4':

    #elif menuChoice == '5':
      
    else:
      id_flag = '++'
      msg = 'ERROR'
      packet = id_flag + msg
      s.sendto(packet, (host, port)) 
    #id_flag = ''
  elif '07' == flag_id:
    #we logged out
    print 'Log out successful! Goodbye!'
    sys.exit()
  elif 'OO' == flag_id:
    msg = getpass.getpass(prompt='Enter new password: ')
    print 'Password Changed!'
    id_flag = 'CC'
    packet = id_flag + msg
    s.sendto(packet, (host, port)) 
  elif 'YU' == flag_id:
    msg = raw_input('Enter your message: ')
    id_flag = 'MU'
    packet = id_flag + msg
    s.sendto(packet, (host, port)) 
    #add packet and flag
    #Somehow, the server will need to keep a record of who I am sending a message to. Maybe a dict? Or just do an array of objects I guess of SENDER and RECV
  elif 'RM' == flag_id:
    print msg
#--All error flags go below here
  #client entered invalid username, ask again
  elif '--' == flag_id:
    print 'Error: Username does not exist. Please try again \n'
    msg = raw_input('Enter your username: ')
    flag_id = '02'
    packet = id_flag + msg
    s.sendto(packet, (host, port)) 
  elif 'LL' == flag_id:
    print 'Error: User is already logged in!'
    sys.exit()
  elif 'BB' == flag_id or 'bb' == flag_id:
    print 'Error: Wrong password. Try again'
    msg = getpass.getpass()
    if flag_id == 'bb':
      id_flag = '04'
    else:
      id_flag = 'KK'
    packet = id_flag + msg
    s.sendto(packet, (host, port)) 
  elif  '-+' == flag_id:
    print 'Error: Messaging error'


  else:
    #print 'CATASTROPHIC ERROR, FLAGID: ' + flag_id
    print 'Error: Session expired, you are logged in elsewhere. Please logout out of the other session or log back in'
    break