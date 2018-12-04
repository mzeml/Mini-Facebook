import socket
import sys
from pprint import pprint
from ast import literal_eval as make_tuple
 
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

#senderToRecv = dict() #{}

#rawAddr = []


#now keep talking with the client
while 1:
    print 'SERVER LOG START: '
    print '\n'
    # receive data from client (data, addr)
    d = s.recvfrom(1024)
    data = d[0] #contains actual message
    addr = d[1] #addr of sender

    # if addr not in rawAddr:
    #   rawAddr.append(addr)

    # print 'Raw address: ' #FIXME: Remove entry when logging out
    # for x in range(len(rawAddr)):
    #   print rawAddr[x]

    #Stores the current flag
    flag_id = data[0:2]
    print flag_id

    msg = data[2:]

    id_flag = flag_id #this helps differntiate what is being sent and recv. Reason I set id_flag to flag_id is for error checking
    

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------   
    
    #Step 1: Client sends a flag of 0. The server knows this means we need to ask client for userName.

    #Step 2: Client sends username, server first checks to see if userNameClient exists in server records
      #if it doesn't, send an error flag. This should result in an error msg and then the previous correct packet maybe? For now, force the user to relog
      #If userNameClient is found on server, temporarily assocaiate the addr with that userName and send a flag that asks for password
    #Step 3: Client sends a password. Server sees if clients addr is associated with a tempAddr
      #If NO match, error out. The client shouldn't have gotten this far with a diff addr
      #if it matches, check to see if password is correct for the uname associated with tempaddress
        #If match, assign client addr to sessionAddr/permAddr. Meaning this addr is assoctaed with a logged in account. Send flag to show menu
        #If NO match, say wrong pw, try again, send again. Have a loop in client for this specific error that asks for pw and sends back to server until pw is correct or 3 failed tries (then break)
    #Step 4: At this point, we are logged in from an addr. Client sends the menu choice of the user. Depending on choice, execute it
    #Step 5 (Logout): Removes user addr from Client object in both temp and session addr. Send user flag that will prompt a goodby msg and a break
    #Step 6 (Change PW): Asks user to send PW again. 3 failed attempts goes to menu (or kills it or nothing, idk)
      #If PW correct, prompt user for new PW twice. Maybe store in Client as tempPw1 and tempPw2 to see if they are identical? For now, just have whatever sent be the new pw
      #Go back to menu
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

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

    elif 'UN' == flag_id:
      
      #FIXME: Find sender uname ans save it in a var
      for index, Client in enumerate(client_list):
        if Client.permAddr == addr[0]:
          sndrName = client_list[index].userName
          break
        else:
          index = -1
      

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
          id_flag == 'NU' #no user, try again

    elif flag_id == 'CM':
      print 'LOG: CHECKING MSGS'
      for index, Client in enumerate(client_list):
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
          #print client_list[index].unread_Msgs[index_2]
          msgPacket = msgPacket + msgArr[index_2]
        del client_list[index].unread_Msgs[:]
      print msgPacket
      id_flag = 'RM'

    #elif... #Sends a message to everyone on the connectedUsers list. Make sure to skip the send-to at the bottom!!! (OR SEND FLAG BACK TO MENU YOU GENIUS)
      #also, ignore the sender (or not, the specs are vauge. Just send it to everyone that's connected)


    elif flag_id == '++':#error, send previous packet again (this one might need tweaking) Maybe keep a copy of the last packet sent?
      print 'ERROR: Unexpected input from client!'
      #FIXME: Client sends wrong menu choice (aka invalid option) triggers this error!!!
    
    else:
      print "ERROR: Unexpected error. Packet loss?"
    
    #DEBUGGING WINDOW

    #sends client what server needs accordinf to the values above
    print 'LOG: Got from client: ' + msg + '    Responding/Sending to client: ' + id_flag + ' addr: ' + addr[0]
    
    #you will need to change this to be able to send messages (or make an if statement if you are afraid of breaking this)
    if flag_id == 'CM':
      packet = id_flag + msgPacket
      s.sendto(packet, addr)
    else:
      s.sendto(id_flag, addr)

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

     
s.close() 
