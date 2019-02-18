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



# function to share the public key to the server
def ssh_key(user):
	key_status = commands.getoutput("yes y | ssh-keygen -b 2048 -t rsa -f /root/.ssh/id_rsa -q -N ''  ")
	print("ssh-keygen...... Generated")
	key_status = commands.getoutput("scp -o StrictHostKeyChecking=no -P "+server_port+
		" /root/.ssh/id_rsa.pub "+user+"@"+server_ip+":.ssh/temp/")
	print("Public key has been copied. Enter the server's password again to apply last modifications")
	key_status = commands.getoutput("ssh "+user+"@"+server_ip+" -p "+server_port+" 'cat .ssh/temp/id_rsa.pub >> .ssh/authorized_keys '")
	print(key_status)





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
				'if [ -d /home/"+group_name+"  ];     \
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
						user_group_status = commands.getoutput("ssh "+server_user+"@"+server_ip+" -p "+server_port+" \
							'useradd "+group_name+" ; \
							echo \""+user_group_pass+"\" | passwd "+group_name+" --stdin ; \
							mkdir /var/www/html/centralizedConsole/web/clients/"+group_name+" ; \
							chmod 700 /var/www/html/centralizedConsole/web/clients/"+group_name+" ; \
							chown "+group_name+" /var/www/html/centralizedConsole/web/clients/"+group_name+"/ ; \
							ln -s /var/www/html/centralizedConsole/web/clients/"+group_name+"/ /home/"+group_name+"/xml ; \
							mkdir /home/"+group_name+"/.ssh ; chmod 700 /home/"+group_name+"/.ssh/ ; \
							chown "+group_name+" /home/"+group_name+"/.ssh ;  \
							touch /home/"+group_name+"/.ssh/authorized_keys ; \
							chmod 600 /home/"+group_name+"/.ssh/authorized_keys ; \
							chown "+group_name+" /home/"+group_name+"/.ssh/authorized_keys ; \
							mkdir  /home/"+group_name+"/.ssh/temp ;  \
							chown "+group_name+" /home/"+group_name+"/.ssh/temp ; ' ")
						ssh_key(group_name)
						# You can print out the user_group_status variable if a promlem is happening to know why.
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
		group_name = str(raw_input("Enter the group's name you want to join to: "))


	else: # ERROR
		option = str(input("\nChoose a correct option.\n1. Create a new group.\n2. Join to a existent group.\n"))
		incorrect_option = True
