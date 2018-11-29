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
  def __init__(self, address, userName, curr_flag, password):
    self.address = address
    self.userName = userName
    self.curr_flag = curr_flag
    self.password = password

client_list = []

#a profile is created and stored on signup. Info is updated when person connects
One_profile = Client('Ones Addr','One','','1')
client_list.append(One_profile)

Two_profile = Client('2Addr','Two','','2')
client_list.append(Two_profile)

Three_profile = Client('3addr','Three','','3')
client_list.append(One_profile)

Four_profile = Client('4addr','Four','','4')
client_list.append(Four_profile)

#connection arrays
client_addr_arr = []
curr_flag = []
curr_flag_index = -1

#user info (if I had more time, I would make a list or an array of arrays to hold the info
userNames = ['One', 'Two', 'Three', 'Four']
userPasswords = ['1', '2', '3', '4']
#When a user logs in, the addr of that machine gets assocate to the login
addrToUser = []
#contains the data last sent to the user in case they send something incorrect
lastSent = []


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
    print [Client.address for Client in client_list if Client.userName == 'Four']

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

    
    #if (addr[0] not in client_addr_arr): #adds the client's addr to array if they haven't connected already
      #client_addr_arr.append(addr[0])
      #adds the flag to an array
      #curr_flag.append(data[0:1])
      #the index of where the address shows up corresponds to the curr_flag index
      #curr_flag_index = client_addr_arr.index(addr[0])
    #else: #it is in the array (note, a dropped client still has their address here, but the flag_id is reset client side (which is a no-no security wise but i'll fix that later). Find a way to set id_flag to 0 in disconnect
     # print '-----Addr found! ' + addr[0]
      #find where the address is in array, use the index location of where that address is in the array, set flag
    #  curr_flag_index = client_addr_arr.index(addr[0])
    #  curr_flag[curr_flag_index] = data[0:1]
      
      #ISSUE: Having the indexes based off addr is problematic when new people show up AND LEAVE!!! the order gets messed up!!!
      # New idea: make a list/array of objects! Each object will contain the addr the user is using, a username slot (to be updated when they sign in), the current flag id (as to have the server up to date on what the client has done)
      
      #print 'Addr was found, curflag: ' + curr_flag[curr_flag_index]
      #flag_id = curr_flag[curr_flag_index]
      
    #pprint(client_addr_arr)
    #curr_flag_index = client_addr_arr.index(addr[0])

    #flag_id = curr_flag[curr_flag_index]
    
    #print flag_id

    


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
      if [Client.userName for Client in client_list if Client.userName == msg]:
        flag_id = '3'
      
      #parse Client object to see if userName is in there. If it is, save this address in tempAddr (ADD THIS TO OBJECT)
      #if msg in userNames:
        #associates the username with the correct pw. Client needs to send the correct pw to gain access
      #  pwIndex = userNames.index(msg)
      #  flag_id = '3'
      else:
        #error on login
        print '### ERROR: Client sent wrong user ###'
        flag_id = '-2'

    elif flag_id == '4': 
      #find addr in Client under tempAddr. If the flag is correct and pw is correct, make this the perm address for the session
      #user has successfully logged in, send flag for menu
      if msg == userPasswords[pwIndex]: 
        flag_id = '5'
        #assocaiates the address with the username
        #if userNames[pwIndex] not in addrToUser:
        #  addrToUser.append(userNames[pwIndex] + ' ' + addr[0])
        #  assocIndex = addrToUser.index(userNames[pwIndex] + ' ' + addr[0])
          
         # print addrToUser[-1]
      else:
        print 'pw error with the arrays'
    elif flag_id == '6': #logout option, deletes user info from connection arrays!
      print 'Log out success!'
      #use the addr[0] to see who is logged in. Remove that entry from the arrays
      #print curr_flag_index
      #print curr_flag[curr_flag_index]
      
      #client_addr_arr.remove(addr[0])
      
      #remove from client_addr_arr
      
      #remove from curr_flag
      
      #remove from addrToUser array too!
      
      #remove curr_flag_index
      
      #remove lastSent
      flag_id = '7'

    elif flag_id == 4: #change vlaue!!!!
      #have user enter password again (needs to be correct to change)
      #have them send new password
      print "hi"

    elif flag_id == '-1':#error, send previous packet again (this one might need tweaking) Maybe keep a copy of the last packet sent?
      print 'ERROR: Unexpected input from client, resending previous packet'
      
    
    else:
      print "ERROR: Unexpected error. Packet loss?"
    
    #testing VS

    #make a copy of the packet here (make sure to associate it correctly!
    #backUpPacket = 
    #if
    #LastSent[curr_flag_index]
    
    #sends client what server needs accordinf to the values above
    print 'Got from client: ' + msg + '    Responding/Sending to client: ' + flag_id + ' addr: ' + addr[0]
    s.sendto(flag_id, addr)

    print 'Server recv this from client: ' + msg
     
s.close() 
