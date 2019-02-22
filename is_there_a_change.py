#!/usr/bin/env python2
# -*- coding: utf-8 -*-

################################################################
# This Code Has Been Developed By                              #
# Eduardo Marquez -- nose238@hotmail.com                       #
################################################################

##################Importing libraries#####################
import time
import commands
import os
from daemon import runner
###########Daemonization part starts######################
class App():
    def __init__(self):
        self.stdin_path = '/dev/null'
        self.stdout_path = '/dev/tty'
        self.stderr_path = '/dev/tty'
        self.pidfile_path =  '/tmp/foo.pid'
        self.pidfile_timeout = 5
    def run(self):
###########Daemonization part ends########################
#---------------------MAIN-------------------------------#
		while True:
			# Read server data.
			tmp_file = open("/root/freeBSD_Files/portServer.txt", "r")
			server_port = tmp_file.read()
			tmp_file.close()
			tmp_file = open("/root/freeBSD_Files/userServer.txt", "r")
			server_user = tmp_file.read()
			tmp_file.close()
			tmp_file = open("/root/freeBSD_Files/ipServer.txt", "r")
			server_ip = tmp_file.read()
			tmp_file.close()
			tmp_file = open("/root/freeBSD_Files/my_group", "r")
			group_name = tmp_file.read()
			tmp_file.close()

			print("It works! " + time.strftime("%c"))
			xml_status = commands.getoutput("ssh "+group_name+"@"+server_ip+" -p "+server_port+"\
				'if [ -f conf.xml  ];     \
				then echo \"existent\"; else echo \"nonexistent\" ; fi ; ' ")
			
			if xml_status == "existent":					
				
				ips_to_change = True
				while ips_to_change:

					ips_to_change = commands.getoutput("ssh "+group_name+"@"+server_ip+" -p "+server_port+"\
						'if [ -f /home/"+group_name+"/ips_to_change.txt  ];     \
						then echo \"existent\"; else echo \"nonexistent\" ; fi ; ' ")
					if ips_to_change == "existent":
						download_txt = commands.getstatusoutput("scp -o StrictHostKeyChecking=no -P "+server_port+
							" "+group_name+"@"+server_ip+":ips_to_change.txt /root/freeBSD_Files/")
						if download_txt[0] != 0:
							print("It was not possible to download the file")
						else:
							ips_to_change = False
							











					elif ips_to_change == "nonexistent":
						ips_to_change = True
						time.sleep(5)
						# This loop is repeted in order to wait to other clients to update the "ips_to_change" file
					else: # ERROR
						print("Connection error\nStatus: " + ips_to_change)
			elif xml_status == "nonexistent":
				print("There is not xml")
			else: # ERROR
				print("It was not possible to connect with the server")
				print("Status: " + xml_status)


			time.sleep(10)
#---------------------MAIN-------------------------------#        
###########Daemonization part starts######################
app = App()
daemon_runner = runner.DaemonRunner(app)
daemon_runner.do_action()
###########Daemonization part ends########################