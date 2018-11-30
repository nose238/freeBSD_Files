#!/usr/bin/env python
# -*- coding: utf-8 -*-

################################################################
# This Code Has Been Developed By                              #
#Jozic Espinoza  -- AKA HackeMatte                             #
#Eduardo Marquez -- nose238@hotmail.com                        #
################################################################
# Start code #
##############

###############################################################
# All routes must be changed, these routes only are for test  #
# this script, the correct route will be the local from the   #
# user's PC                                                   #
###############################################################

#*************************************************************#
#*************************************************************#
# ***   ***  ***  *** IMPORTANT NOTES  **** *** *** *** ** ** #
# 1. Verify that .ssh/ directory has permission 700 as in the #
# server as in the client                                     #
# 2. Verify that id_rsa file has permission 600 in the client #
# 3. Verify that authorized_keys has permission 600 in the    #
# server                                                      #
# 4. "f" variable can be used to debug bash code              #
#*************************************************************#

import commands
import socket


print("You can press ctrl + c in any moment to cancel this prossess.\nPress enter to continue.")
# Public key is generated
f = commands.getoutput("yes y | ssh-keygen -b 2048 -t rsa -f /root/.ssh/id_rsa -q -N '' ; chmod 600 /root/.ssh/id_rsa ") 

### Get all client informaton and write .txt's which contain it 
pcName = socket.gethostname()
userName = raw_input("Enter your user name (it must be able to access through ssh protocol): ")
passwd = raw_input("Enter your passwd: ")
groupName = raw_input("Enter the group name to create database: ")
ipAddress = raw_input("Enter your ip address: ")
port = raw_input("Enter your port (SSH): ")
description = raw_input("Enter a description: ")
file = open('/root/freeBSD_Files/groupName.txt', 'w')
file.write(groupName) #Change the hostname on data document
file.close()
file = open('/root/freeBSD_Files/ipHost.txt', 'w')
file.write(ipAddress)
file.close()
file = open('/root/freeBSD_Files/userName.txt', 'w')
file.write(userName)
file.close()
file = open('/root/freeBSD_Files/passwd.txt', 'w')
file.write(passwd)
file.close()
file = open('/root/freeBSD_Files/description.txt', 'w')
file.write(description)
file.close()
file = open('/root/freeBSD_Files/hostName.txt', 'w')
file.write(pcName) #Change the pcś ip address on data document
file.close()
file = open('/root/freeBSD_Files/port.txt', 'w')
file.write(port)
file.close()

###### Format and write client information
f = open('/root/freeBSD_Files/groupName.txt', 'r') #Variable for client name
line=f.readline()
if line:
    name=line
f = open('/root/freeBSD_Files/ipHost.txt', 'r') #Variable for ip address
line=f.readline()
if line:
    ip=line
f = open('/root/freeBSD_Files/hostName.txt', 'r') #Variable for host name
line=f.readline()
if line:
    host=line
file = open('/root/freeBSD_Files/clientInformation.txt', 'w')
file.write(host+"|"+ip+"|"+name+"|") #give the correct format to data document
file.close()
###### Format and write client credentials
file = open('/root/freeBSD_Files/clientCredentials.txt', 'w')
file.write(ip+"|"+userName+"|"+passwd+"|"+port+"|"+groupName+"\n")
file.close()
###### Reading server data
file = open("/root/freeBSD_Files/portServer.txt", "r")
portServer = file.read()
file.close()
file = open("/root/freeBSD_Files/userServer.txt", "r")
userServer = file.read()
file.close()
file = open("/root/freeBSD_Files/ipServer.txt", "r")
ipServer = file.read()
file.close()
###### Send Public key to the server. IT NEEDS TO TYPE 2 TIMES PASSWORD
print("Enter the server's password to copy public key")

# It generates a temp file with id_rsa.pub. Then it is added to the server's authorized_keys file
f = commands.getoutput("scp -o StrictHostKeyChecking=no -P "+portServer+" /root/.ssh/id_rsa.pub "+userServer+"@"+ipServer+":.ssh/temp/")
print(f)
print("Public key has been copied. Enter the server's password again to apply last modifications")
f = commands.getoutput("ssh "+userServer+"@"+ipServer+" -p "+portServer+" 'cat .ssh/temp/id_rsa.pub >> .ssh/authorized_keys '")
print(f)

###### Once public key is on the server, the group directory is created and  copy information.
	# verify if group and ip directories exist.
f = commands.getoutput("ssh "+userServer+"@"+ipServer+" -p "+portServer+"                               \
	'if [ -d /var/www/html/centralizedConsole/web/clients/"+groupName+"  ];                             \
 		then echo \"This group already exists... Verifying if IP and user\" ;                           \
 	else echo \"Group does not exist. Directory has been created\" ;                                    \
 		mkdir /var/www/html/centralizedConsole/web/clients/"+groupName+";                               \
 	fi ;                                                                                                \
 	if [ -d /var/www/html/centralizedConsole/web/clients/"+groupName+"/"+ip+" ] ;                       \
 		then echo \"IP directory exist\" ;                                                              \
 	else mkdir /var/www/html/centralizedConsole/web/clients/"+groupName+"/"+ip+" ;                      \
 		echo \"IP directory has been created.\" ;                                                       \
 	fi;                                                                                               '")
print(f)

	# Copy all files onto server
f = commands.getoutput("scp -P "+portServer+" /root/freeBSD_Files/clientInformation.txt                 \
	/root/freeBSD_Files/description.txt /root/freeBSD_Files/clientCredentials.txt                       \
	"+userServer+"@"+ipServer+":/var/www/html/centralizedConsole/web/clients/"+groupName+
	"/"+ip+"/" )
print(f)

# Client's credential is added in clientsCredentials File
f = commands.getoutput("ssh "+userServer+"@"+ipServer+" -p "+portServer+" 'cat /var/www/html/centralizedConsole/web/clients/"+
	groupName+"/"+ip+"/clientCredentials.txt >> /var/www/html/centralizedConsole/web/clients/clientsCredentials '" )
print(f)