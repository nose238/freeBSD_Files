#!/usr/bin/env python
# -*- coding: utf-8 -*-

################################################################
# This Code Has Been Developed By                              #
#Jozic Espinoza  -- AKA HackeMatte                             #
#Eduardo Marquez                                               #
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
#*************************************************************#

#####Operating System libraries#####
import commands
#####End Operating System libraries# section####
print("You can press ctrl + c in any moment to cancel this prossess.\nPress enter to continue.")
#this line could be usefull, . To create public key
# f = commands.getoutput("ssh-keygen -b 2048 -t rsa -f /root/.ssh/id_rsa -q -N '' ; chmod 777 /root/.ssh/id_rsa ") 
userName = raw_input("Enter your user name (it must be able to access through ssh protocol): ")
passwd = raw_input("Enter your passwd: ")
groupName = raw_input("Enter the group name to create database: ")
ipAddress = raw_input("Enter your ip address: ")
#interfaceName = raw_input("Enter the network interface name to start diagnostic: ")
########create files#######
#file = open('/root/python/interfaceName.txt', 'w')
#file.write(interfaceName) #Change the hostname on data document
#file.close()
file = open('/root/python/clientName.txt', 'w')
file.write(groupName) #Change the hostname on data document
file.close()
#ipCommand="ifconfig "+str(interfaceName)+" | grep \"inet:\" | cut -d ':' -f 2 | cut -d ' ' -f 1"
#getIp=commands.getoutput(ipCommand)
file = open('/root/python/ipHost.txt', 'w')
#file.write(getIp) #Change the hostname on data document
file.write(ipAddress)
file.close()
file = open('/root/python/userName.txt', 'w')
file.write(userName)
file.close()
file = open('/root/python/passwd.txt', 'w')
file.write(passwd)
file.close()
######Reading server data
file = open("/root/python/portServer.txt", "r")
portServer = file.read()
file.close()
file = open("/root/python/userServer.txt", "r")
userServer = file.read()
file.close()
file = open("/root/python/ipServer.txt", "r")
ipServer = file.read()
file.close()
######Send Public key to the server. IT NEEDS TO TYPE 2 TIMES PASSWORD
print("Enter the server's password to copy public key")
f = commands.getoutput("scp -P "+portServer+" /root/.ssh/id_rsa.pub "+userServer+"@"+ipServer+":.ssh/temp/")
print(f)
print("Public key has been copied. Enter the server's password again to apply last modifications")
f = commands.getoutput("ssh "+userServer+"@"+ipServer+" -p "+portServer+" 'cat .ssh/temp/id_rsa.pub >> .ssh/authorized_keys '")
print(f)

