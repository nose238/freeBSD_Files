#!/usr/bin/env python
# -*- coding: utf-8 -*-

################################################################
# This Code Has Been Developed By                              #
# Eduardo Marquez -- nose238@hotmail.com                       #
################################################################
import commands

# Read server data.
tmp_file = open("portServer.txt", "r")
server_port = tmp_file.read()
tmp_file.close()
tmp_file = open("userServer.txt", "r")
server_user = tmp_file.read()
tmp_file.close()
tmp_file = open("ipServer.txt", "r")
server_ip = tmp_file.read()
tmp_file.close()



# main menu.
print("\tWelcome to the Warriors Labs' Cenrtalized Console configuration.")
option = str(input("Choose an option:\n1. Create a new group.\n2. Join to a existent group.\n"))
incorrect_option = True
while incorrect_option:
	
	if option == "1":
		incorrect_option = False
		print("You chose Create a new group.")

		# This loop verify if the group name exists.
		group_exists = True
		while group_exists: 
			group_name = str(raw_input("Enter the group's name: "))
			group_status = commands.getoutput("ssh "+server_user+"@"+server_ip+" -p "+server_port+"\
				'if [ -d /var/www/html/centralizedConsole/web/clients/"+group_name+"  ];     \
				then echo \"existent\"; else echo \"nonexistent\" ; fi ; ' ")
			print(group_status)
			if group_status == "existent":
				group_exists = True
				print("This group has already been created, select another name or prees 'ctrl + z', \
				re-run this code and join to a existent one")
			elif group_status == "nonexistent":
				group_exists = False
				print("CREAR GRUPO")

			else:
				print("Unexpected error")
				exit() 






		continue
	elif option == "2": 
		incorrect_option = False
		print("You chose Join to a existent group.")


		continue
	else:
		option = str(input("Choose a correct option.\n1. Create a new group.\n2. Join to a existent group.\n"))
		incorrect_option = True
