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
One_profile = Client('eec','One','','1')
client_list.append(One_profile)

Two_profile = Client('Bla','Two','','2')
client_list.append(Two_profile)

Three_profile = Client('cccc','Three','','3')
client_list.append(One_profile)

Four_profile = Client('FER','Four','','4')
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
    
    #client_list.append(Client(addr[0],'TEST','-1')
    
    #This bad boy finds where the userName matches the object in the list and outputs the address. USE IT TO UPDATE ADDRESS WHEN THEY LOGIN
    print [Client.address for Client in client_list if Client.userName == 'Four']
    
    
    
    if (addr[0] not in client_addr_arr): #adds the client's addr to array if they haven't connected already
      client_addr_arr.append(addr[0])
      #adds the flag to an array
      curr_flag.append(data[0:1])
      #the index of where the address shows up corresponds to the curr_flag index
      curr_flag_index = client_addr_arr.index(addr[0])
    else: #it is in the array (note, a dropped client still has their address here, but the flag_id is reset client side (which is a no-no security wise but i'll fix that later). Find a way to set id_flag to 0 in disconnect
      print '-----Addr found! ' + addr[0]
      #find where the address is in array, use the index location of where that address is in the array, set flag
      curr_flag_index = client_addr_arr.index(addr[0])
      curr_flag[curr_flag_index] = data[0:1]
      
      #ISSUE: Having the indexes based off addr is problematic when new people show up AND LEAVE!!! the order gets messed up!!!
      # New idea: make a list/array of objects! Each object will contain the addr the user is using, a username slot (to be updated when they sign in), the current flag id (as to have the server up to date on what the client has done)
      
      #print 'Addr was found, curflag: ' + curr_flag[curr_flag_index]
      #flag_id = curr_flag[curr_flag_index]
      
    #pprint(client_addr_arr)
    #curr_flag_index = client_addr_arr.index(addr[0])

    flag_id = curr_flag[curr_flag_index]
    
    #print flag_id

    msg = data[1:]


    #if we have no data, we're done here 
    if not data: 
        print 'Error: No Data!'
        break

    if '0' == flag_id: 
        #needs user, client will prompt user for userName
        flag_id = '1'
        
    elif '2' == flag_id:
      #Gonna somehow associate the userName with the password. I know we have the object, but anyone can attempt a login, so we do that later
      
      
      #parse Client object to see if userName is in there. If it is, save this address in tempAddr (ADD THIS TO OBJECT)
      if msg in userNames:
        #associates the username with the correct pw. Client needs to send the correct pw to gain access
        pwIndex = userNames.index(msg)
        flag_id = '3'
      else:
        #error on login
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
    
    

    #make a copy of the packet here (make sure to associate it correctly!
    #backUpPacket = 
    #if
    #LastSent[curr_flag_index]
    
    #sends client what server needs accordinf to the values above
    print 'Got from client: ' + msg + '    Responding/Sending to client: ' + flag_id + ' addr: ' + addr[0]
    s.sendto(flag_id, addr)

    print 'Server recv this from client: ' + msg
     
s.close() 
