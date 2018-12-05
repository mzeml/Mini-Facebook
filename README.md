# Mini-Facebook Messaging System

In this project, I used Mininet to emulate a network topology consisting of one server and three client nodes and implement a simple Facebook application on top of this topology using a client - server model. Clients run client codes to make use of the capabilities they are provided with and the server is responsible for authenticating users, receiving posts and messages from users and sending them to the proper intended recipient.

For the record, my instructor called this the Facebook project, I think it is more of like Snapchat messaging

## Specifications to Meet

0. Nothing should be stored client-side. I took this to mean no userdata or passwords.
1. Whenever a user connects to the server, they should be asked for their username and password.
2. Username should be entered as clear text but passwords should not (should be either obscured or hidden).
3. User should log in successfully if username and password are entered correctly. A set of username/password pairs are hardcoded on the server side.
4. User should be provided with a menu. The menu includes all possible options (commands) user can use and how they can use them. These options include Logout, Change Password, etc. As you add functionality, you can add new options to this menu.
5. Change Password: User should be able to change their password. To do this, old and new passwords should be entered (neither as clear text).
6. Logout: User should be able to logout and close their connections with the server. 
7. A user should see their messages in real - time (live) if they are online when someone sends them messages.
8. Send Message: A user should be able to send a private message to any other user (whether or not the recipient of the message is online) .
9. View Count of Unread Messages: A user should see the number of unread messages when logging in.
10. Read Unread Messages: A user should be able to read all unread messages. 311. Send Broadcast message: A user should be able to send a message to the server which only forwards to all clients who are currently connected.

I managed to get all but 7 implemented. 7 would require threading, which is something I did not have time to do.

## How it works

0. You need to have a Mininet VM setup with a local NAT
1. SSH into Mininet and run 'bash runTopol.sh'
2. A few windows will pop up. Find the one called S1 and run the server code
3. In the windows that start with C, run the client code
4. Login with username and password, select menu options, and enjoy

## Issues

This project was done in 2 parts, with each part taking me roughly 3 days to do (on top of all my other classes). This means I was rushed which results in some issues.

Actually, there are a LOT of issues with my implementation: Overhead, security, general ugly code, etc.

I tried to handle errors as best as I could, but I didn't account for every case.

Overhead: There are a lot of loops, which means this code does not scale well at all. It meets the specs, which all that mattered

Security: No encryption and an attacker can spoof an address to gain login, but this wasn't within scope of the project

Ugly code: You can look at all the 'flag_id' and you will understand why this is ugly. Also, I could have done a better job with variable name consistency, but considering a significant portion of the project was done well past midnight, I ask for some slack

All in all, it works (for the most part)
