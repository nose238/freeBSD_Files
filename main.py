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
print("\n\n\tWelcome to the Warriors Labs' Cenrtalized Console configuration.")
print("For security cuestions you'll have to enter the server password some times when it's needed.\n")
option = str(raw_input("Choose an option:\n1. Create a new group.\n2. Join to a existent group.\n"))
incorrect_option = True
while incorrect_option:
	
	if option == "1":
		incorrect_option = False
		print("\nYou chose Create a new group.")
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
			
			# if the directory does not exist then it will be created together with a user for the group
			elif group_status == "nonexistent":
				print("We can create a directory with this name ")
				group_exists = False
				print("Your group '"+group_name+"' will be created")
				pass_doesnot_match = True
				# This loop just do the confirmation of the password
				while pass_doesnot_match:
					user_group_pass = raw_input("Your user is '"+group_name+"'. Write a password to this user: ")
					confirm_pass = raw_input("Enter your password again: ") 
					# if passwords match then a user and its directory home are created 
					if user_group_pass == confirm_pass:
						pass_doesnot_match = False
						print("Passwords match!!! We can continue with the configuration")
						user_group_status = commands.getoutput("ssh "+server_user+"@"+server_ip+" -p "+server_port+"\
							'useradd "+group_name+" -d /var/www/html/centralizedConsole/web/clients/"+group_name+" ; \
							echo \""+user_group_pass+"\" | passwd "+group_name+" --stdin ; ' ")
						print(user_group_status)
					else:
						print("Passwords don't match.")
						# Loop is repeted
			else: # ERROR
				print("Unexpected error")
				print("Status: " + str(group_status))
				exit() 
	elif option == "2": 
		incorrect_option = False
		print("\nYou chose Join to a existent group.")
		continue

	else: # ERROR
		option = str(input("\nChoose a correct option.\n1. Create a new group.\n2. Join to a existent group.\n"))
		incorrect_option = True
