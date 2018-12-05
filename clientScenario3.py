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
  elif '05' == flag_id or flag_id == '15' or flag_id == 'RM' or flag_id == 'NU': #or add another flag indicating that unread messages exist
    print '\n'
    print 'You have' + reply[2:4] + ' unread messages \n' #It only 

    if 'RM' == flag_id: #Outputs messages
      print reply[4:]
    elif 'NU' == flag_id:
      print 'Error: User does not exist!'
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
    elif menuChoice == '3': #want to send message.
      #ask who to send it to. Server will respond with a flag "X" if person is a valid user. Else, flag Y tells client not valid, try again
      msg = raw_input('Enter the username of who you want to send the message to: ')
      raw = raw_input('Enter your message: ')
      msg = msg + ': ' + raw #fixme: This sends the RECV uname plus the message. This is ok, but you need to change it so its the SENDER uname when saving the message server side!
      id_flag = 'UN'
      #print 'Message to server ' + msg
      packet = id_flag + msg
      s.sendto(packet, (host, port))
      #break
    elif menuChoice == '4':
      msg = raw_input('Enter message you want to broadcast to online users: ')
      id_flag = 'br'
      packet = id_flag + msg
      s.sendto(packet, (host, port))
    elif menuChoice == '5':
      id_flag = 'CM'
      msg = 'CHCKMSG'
      packet = id_flag + msg
      s.sendto(packet, (host, port))
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

#--All error flags go below here--------
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
  elif '-+' == flag_id:
    print 'Error: Messaging error'

  else:

    print 'Error: Session expired. Please logout out and log back in'
    break