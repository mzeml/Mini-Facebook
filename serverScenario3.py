import socket
import sys
from pprint import pprint
 
HOST = '10.0.0.4'
PORT = 8888 # Arbitrary non-privileged port
 
#  UDP socket
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

class Client:
  def __init__(self, userName, password, permAddr, tempAddr, tempRecv, unreadCount):
    self.userName = userName #holds the userName of the profile
    self.password = password #password for the associated profile
    self.permAddr = permAddr #User has logged in, this is the address for the session
    self.tempAddr = tempAddr #When valid username given, save client's address to verify later
    self.tempRecv = tempRecv #store the userName of the reciver of the message going out
    self.unreadCount = unreadCount #an int counting how many unread messages
    self.unread_Msgs = [] #stores all the messages sent to user

#Holds all the profiles
client_list = []

#a profile is created and stored on signup. Info is updated when person connects
One_profile = Client('One','1','','','',0)
client_list.append(One_profile)

Two_profile = Client('Two','2','','','',0)
client_list.append(Two_profile)

Three_profile = Client('Three','3','','','',0)
client_list.append(Three_profile)

Four_profile = Client('Four','4','','','',0)
client_list.append(Four_profile)

connected_users = []

#now keep talking with the client
while 1:
    print 'SERVER LOG START: '
    print '\n'
    # receive data from client (data, addr)
    d = s.recvfrom(1024)
    data = d[0] #contains actual message
    addr = d[1] #addr of sender

    #Stores the current flag
    flag_id = data[0:2]
    print flag_id

    msg = data[2:]
    unreadMsgCnt = 0
    for index, Client in enumerate(client_list):
      if Client.tempAddr == addr[0] or Client.permAddr == addr[0]:
          unreadMsgCnt = client_list[index].unreadCount #bug is this evernually outputs [] when empty
          break

    id_flag = flag_id #this helps differntiate what is being sent and recv. Reason I set id_flag to flag_id is for error checking

    #if we have no data, we're done here 
    if not data: 
        print '###ERROR: No Data in client packet###'
        break

    #new client connected, send back a request for userName
    if '00' == flag_id: 
        #flag_id of 1 prompts client for userName
        id_flag = '01'
    #userName recieved    
    elif '02' == flag_id:
      #Checks if valid userName
      for index, Client in enumerate(client_list):
        print 'LOOKING FOR: ' + msg
        if Client.userName == msg:
          print 'LOG: Valid user found: ' + client_list[index].userName
          id_flag = '03'
          print 'LOG: Client sent valid username. Storing temp addr. Sending password request'
          client_list[index].tempAddr = addr[0]
          break
        else:
          #Keeps searching. If nothing gets found, then flag_id remains '-' (indicating no user found)
          index = -1
          id_flag = '--'
          print 'LOG: User not yet found, trying again...'
    elif flag_id == '04': 
      
      #find addr in Client under tempAddr. If the flag is correct and pw is correct, make this the perm address for the session
      #user has successfully logged in, send flag for menu
      #Checks to see if someone already logged in (Note: This might break if a user quits abruptly [no logout]. In that case, comment this out heh) Logical fix is a timeout
      #Searches list of Clients to see if the client we are talking to is the last client we just talked to for this userName
      #if the password matches when the tempAddr matches, make tempAddr the perm addr

      for index_2, Client in enumerate(client_list):
        if Client.password == msg and Client.tempAddr == addr[0]:
          client_list[index_2].permAddr = addr[0]
          connected_users.append(addr[0])
          id_flag = '05'
          #unreadMsgCnt = client_list[index_2].unreadCount
          print 'LOG: Password and username match, associating tempAddr to permAddr for this session'
          break
        else:
          index_2 = -1
          id_flag = 'bb'
          print 'LOG: Password not matched, trying to find [1]...'

    elif flag_id == '06': #logout option, deletes user info from connection arrays!
      for index, Client in enumerate(client_list):
        if Client.permAddr == addr[0]:
          client_list[index].tempAddr = ''
          client_list[index].permAddr = ''
          connected_users[connected_users.index(addr[0])] = ''
          print 'LOG: Log out success!'
          id_flag = '07'
          break
        else:
          #Keeps searching. If nothing gets found, then id_flag remains '-' (indicating no user found)
          index = -1
          id_flag = '~~' #Basically, if the client gets this, something is very wrong
          print 'LOG: Addr match not yet found, trying again...'

    elif flag_id == '08':
      #have user enter password again (needs to be correct to change)
      #have them send new password

      for index, Client in enumerate(client_list):
        if Client.permAddr == addr[0]:
          id_flag = '09'
          print 'LOG: Correct client, Asking for old password'
          break
        else:
          index = -1
          id_flag = '~'
          #print 'LOG: Password not matched, trying to find [2] -> ' + msg
          #print msg
    
    #Check PW, if correct, ask for new
    elif flag_id == 'KK':
      for index, Client in enumerate(client_list):
        if Client.permAddr == addr[0] and Client.password == msg:
          print 'LOG: Old password correct, asking client for new one'
          id_flag = 'OO'
          break
        else:
          #Keeps searching. If nothing gets found, then id_flag remains '-' (indicating no user found)
          index = -1
          id_flag = 'BB' #FIXEME Have this go to wrong PW case!!!!
          print 'LOG: Password not matched, trying to find [2] -> ' + msg
          #print 'LOG: Addr match not yet found, trying again...'

    elif flag_id == 'CC':
      for index, Client in enumerate(client_list):
        if Client.permAddr == addr[0]:
          client_list[index].password = msg
          id_flag = '05'
          print 'LOG: Password successfully changed, sending client to menu'
          break
        else:
          index = -1
          id_flag = 'LL'

    elif 'UN' == flag_id: #Client has sent us the username and the message to be sent
      
      #gets the username of the sender so we can append to message (so recv knows who sent it)
      for index, Client in enumerate(client_list):
        if Client.permAddr == addr[0]:
          #unreadMsgCnt = client_list[index].unreadCount
          sndrName = client_list[index].userName
          break
        else:
          index = -1
          id_flag = 'NU' #No user found, try again

      #Step 2: Remove the recv name from the message. Find the uName of the recv and append the message to their unreads
      msgTorecv = msg.split(':')[1]
      msg = msg.split(':')[0]
      for index, Client in enumerate(client_list):
        print 'LOOKING FOR: ' + msg
        if Client.userName == msg:
          print 'LOG: Valid recv found, storing in temp recv (RECV ->): ' + client_list[index].userName
          msgTorecv = sndrName + ': ' + msgTorecv + '\n'
          client_list[index].unread_Msgs.append(msgTorecv)
          client_list[index].unreadCount = client_list[index].unreadCount + 1
          id_flag = '15'
          break
        else:
          index = -1
          id_flag = 'NU' #no user, try again

    elif flag_id == 'CM': #Checks unread messages and clears them
      print 'LOG: CHECKING MSGS'
      for index, Client in enumerate(client_list): #gets the index we need
        if Client.permAddr == addr[0]:
          break
        else:
          index = -1

      msgArr = client_list[index].unread_Msgs
      msgPacket = ''
      if not msgArr:
        msgPacket = 'No messages! \n'
      else:
        for index_2 in range(0, len(msgArr)):

          msgPacket = msgPacket + msgArr[index_2]
        del client_list[index].unread_Msgs[:]
        client_list[index].unreadCount = 0
        unreadMsgCnt = 0
      print msgPacket
      id_flag = 'RM'

    elif flag_id == 'br':
      #first, add the uName of sender to the msg. Find uname by searching where addr[0] = permAddr
      for index, Client in enumerate(client_list):
        if Client.permAddr == addr[0]:
          senderName = client_list[index].userName
          #unreadMsgCnt = client_list[index].unread_Msgs
          break
        else: 
          index = -1
          senderName = 'ERRORNAME'
          #maybe add an error flag

      broadcast = 'BROADCAST FROM ' + senderName + ': ' + msg + '\n'
      for index_2 in range(0, len(connected_users)):
        for index_3, Client in enumerate(client_list):
          if Client.permAddr == connected_users[index_2] and Client.permAddr != addr[0]: #sends to all but itself
            print 'LOG: FOUND CONNECTED USER'
            client_list[index_3].unread_Msgs.append(broadcast)
            client_list[index_3].unreadCount = client_list[index_3].unreadCount + 1
      #now iterate through online users and add the above message to their unread messages attribute (this will also send the message back to sender)
      id_flag = '15'
    elif flag_id == '++':#error, send previous packet again (this one might need tweaking) Maybe keep a copy of the last packet sent?
      print 'ERROR: Unexpected input from client!'
      #FIXME: Client sends wrong menu choice (aka invalid option) triggers this error!!!
    
    else:
      print 'ERROR: Unexpected error'
    
    #DEBUGGING CODE-----------------------------------------------------

    #sends client what server needs accordinf to the values above
    print 'LOG: Got from client: ' + msg + '    Responding/Sending to client: ' + id_flag + ' addr: ' + addr[0]
    
    print unreadMsgCnt 
    if unreadMsgCnt > 9: #incase the values go over
      unReadStr = '+' + 9
    else:
      unReadStr = ' ' + str(unreadMsgCnt)
    if flag_id == 'CM':
      packet = id_flag + unReadStr + msgPacket
      s.sendto(packet, addr)
    else:
      packet = id_flag + unReadStr
      print 'LOG: PACKET ' + packet
      s.sendto(packet, addr)

    print 'LOG: Got from client: ' + msg + '    Responding/Sending to client: ' + packet + ' addr: ' + addr[0]
    print 'LOG: Server recv this from client: ' + msg
    print 'LOG: CURRENT VALUES OF ARRAYS'
    print 'permaddr: '
    print [Client.permAddr for Client in client_list]
    print 'tempaddr: '
    print [Client.tempAddr for Client in client_list]
    print 'user: '
    print [Client.userName for Client in client_list]
    print 'pw: '
    print [Client.password for Client in client_list]
    print 'Online users'
    pprint(connected_users)
    print 'ALL msgs'
    print [Client.unread_Msgs for Client in client_list]
    print 'UnreadsCnt for user'
    print [Client.unreadCount for Client in client_list]
     
s.close() 
