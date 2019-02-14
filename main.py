#!/usr/bin/env python2
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
print("For security cuestions you'll have to enter the server password some times when it's needed.\n")
option = str(raw_input("Choose an option:\n1. Create a new group.\n2. Join to a existent group.\n"))
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
			print("This group is " + group_status)
			if group_status == "existent":
				group_exists = True
				print("This group has already been created, select another name or prees 'Ctrl + z', \
				re-run this code and join to a existent one")
			# if the directory does not exist then it is created
			elif group_status == "nonexistent":
				print("We can create a directory with this name ")
				group_exists = False
				group_directory_status = commands.getoutput("ssh "+server_user+"@"+server_ip+" -p"+server_port+"\
					'mkdir /var/www/html/centralizedConsole/web/clients/"+group_name+" ; ' ")
				# Verify if the directory has been created successfully
				if group_directory_status == "":
					print("Your group '"+group_name+"' has been created")
					pass_doesnot_match = True
					while pass_doesnot_match:
						user_group_pass = raw_input("Your user is '"+group_name+"'. Write a password to this user: ")
						confirm_pass = raw_input("Enter your password again: ") 
						if user_group_pass == confirm_pass:
							pass_doesnot_match = False
							print("Passwords match!!!")






						else:
							print("Passwords don't match.")
							# Loop is repeted
				else: # ERROR
					print("Unexpected error")
					print("Staus: " + str(group_directory_status))
					exit()
			else: # ERROR
				print("Unexpected error")
				print("Status: " + str(group_status))
				exit() 
		continue

	elif option == "2": 
		incorrect_option = False
		print("You chose Join to a existent group.")
		continue

	else: # ERROR
		option = str(input("Choose a correct option.\n1. Create a new group.\n2. Join to a existent group.\n"))
		incorrect_option = True
