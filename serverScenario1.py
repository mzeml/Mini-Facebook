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
  def __init__(self, userName, password, permAddr, tempAddr):
    self.userName = userName
    self.password = password
    self.permAddr = permAddr
    self.tempAddr = tempAddr

#Holds all the profiles
client_list = []

#a profile is created and stored on signup. Info is updated when person connects
One_profile = Client('One','1','','')
client_list.append(One_profile)

Two_profile = Client('Two','2','','')
client_list.append(Two_profile)

Three_profile = Client('Three','3','','')
client_list.append(Three_profile)

Four_profile = Client('Four','4','','')
client_list.append(Four_profile)

#now keep talking with the client
while 1:
    print '\n'
    # receive data from client (data, addr)
    d = s.recvfrom(1024)
    data = d[0] #contains actual message
    addr = d[1] #addr of sender

    #Stores the current flag
    flag_id = data[0:1]
    msg = data[1:]
    
    #client_list.append(Client(addr[0],'TEST','-1')
    
    #This bad boy finds where the userName matches the object in the list and outputs the address. USE IT TO UPDATE ADDRESS WHEN THEY LOGIN
    #print [Client.address for Client in client_list if Client.userName == 'Four']

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

#READMEEEEEE: Fix ALL OF THE IF ELSE STATEMENTS WHERE YOU USED THE BOTCHED PARSER. Else you'll never send the right flags back!!!
    #if we have no data, we're done here 
    if not data: 
        print '###ERROR: No Data in client packet###'
        break

    #new client connected, send back a request for userName
    if '0' == flag_id: 
        #flag_id of 1 prompts client for userName
        flag_id = '1'
    
    #userName recieved    
    elif '2' == flag_id:

      #Gonna somehow associate the userName with the password. I know we have the object, but anyone can attempt a login, so we do that later
      #if [Client.userName for Client in client_list if Client.userName == msg]:
      #  Client.tempAddr = addr[0]

      #Checks if valid userName
      for index, Client in enumerate(client_list):
        if Client.userName == msg:
          print 'LOG: Valid user found: ' + client_list[index].userName
          flag_id = '3'
          print 'LOG: Client sent valid username. Storing temp addr. Sending password request'
          client_list[index].tempAddr = addr[0]
          break
        else:
          #Keeps searching. If nothing gets found, then flag_id remains '-' (indicating no user found)
          index = -1
          flag_id = '-'
          print 'LOG: User not yet found, trying again...'
      #print 'LOG: Client sent valid username. Storing temp addr. Sending password request'
      
      #print 'TEMP ADDR: ' + client_list[index].tempAddr
      #else:
      #  #error on login, ask for username again
      #  print '### ERROR: Client sent wrong user ###'
      #  flag_id = '-'

    elif flag_id == '4': 
      #find addr in Client under tempAddr. If the flag is correct and pw is correct, make this the perm address for the session
      #user has successfully logged in, send flag for menu
      #if [Client.userName for Client in client_list if Client.password == msg] and [Client.userName for Client in client_list if Client.tempAddr == addr[0]]:
      print 'LOG: ELIF FLAG ID 4'

      #Searches list of Clients to see if the client we are talking to is the last client we just talked to for this userName
      
      #if the password matches when the tempAddr matches, make tempAddr the perm addr
      for index_2, Client in enumerate(client_list):
        if Client.password == msg and Client.tempAddr == addr[0]:
          client_list[index_2].permAddr = addr[0]
          flag_id = '5'
          print 'LOG: Password and username match, associating tempAddr to permAddr for this session'
          break
        else:
          index_2 = -1
          flag_id = '-' #FIXEME Have this go to wrong PW case!!!!
          print 'LOG: Password not matched, trying to find...'
        
        
        
        #Checks to see if someone already logged in (Note: This might break if a user quits abruptly [no logout]. In that case, comment this out heh) Logical fix is a timeout
        
        
        
        #if Client.permAddr != '' :
        #  print 'ERROR: Someone else logged in'
        #  flag_id = 'L'
        #else:
          #Client.permAddr = addr[0]
          #flag_id = '5'

        #I changed it back since if someone drops out, login access to the person dies with them. New logins boot old user though...
        #Client.permAddr = addr[0]
        #flag_id = '5'
        #print 'PERM ADDR: ' + Client.permAddr
        #print 'LOG: Correct password and username combo...saving address'
      #else:
        #print 'ERROR: Wrong password \n'
    elif flag_id == '6': #logout option, deletes user info from connection arrays!
      for index, Client in enumerate(client_list):
        if Client.permAddr == addr[0]:
          client_list[index].tempAddr = ''
          client_list[index].permAddr = ''
          print 'LOG: Log out success!'
          flag_id = '7'
          break
        else:
          #Keeps searching. If nothing gets found, then flag_id remains '-' (indicating no user found)
          index = -1
          flag_id = '~' #Basically, if the client gets this, something is very wrong
          print 'LOG: Addr match not yet found, trying again...'

    elif flag_id == '8':
      #have user enter password again (needs to be correct to change)
      #have them send new password

      #checks to see if we're talking to the correct address
      if [Client.userName for Client in client_list if Client.permAddr == addr[0]]:
        flag_id = '9'
      else:
        flag_id = 'L'
    
    #We got the correct password, now ask client for new one
    elif flag_id == 'K':
      if [Client.userName for Client in client_list if Client.permAddr == addr[0]]:
        flag_id = 'O'
        print '----------------- ' + flag_id
      else:
        flag_id = 'L'

    elif flag_id == 'C':
      for index, Client in enumerate(client_list):
        if Client.permAddr == addr[0]:
          break
        else:
          index = -1
        print client_list[1].permAddr
      #if [index for Client in client_list if Client.permAddr == addr[0]]:
      #  print index + ' : INNNNNN'
      #  Client.password = msg
      #  print 'New pw: ' + Client.password + ' For user: ' + Client.userName
        flag_id = '5'
      else:
        flag_id = 'L'


    elif flag_id == '+':#error, send previous packet again (this one might need tweaking) Maybe keep a copy of the last packet sent?
      print 'ERROR: Unexpected input from client, resending previous packet'
      
    
    else:
      print "ERROR: Unexpected error. Packet loss?"
    
    #DEBUGGING WINDOW
    #sends client what server needs accordinf to the values above
    print 'LOG: Got from client: ' + msg + '    Responding/Sending to client: ' + flag_id + ' addr: ' + addr[0]
    s.sendto(flag_id, addr)

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


     
s.close() 
