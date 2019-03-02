#!/usr/bin/env python2
# -*- coding: utf-8 -*-

################################################################
# This Code Has Been Developed By                              #
# Eduardo Marquez -- nose238@hotmail.com                       #
################################################################

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
			
			# Verify if we have to do a "ctrl + z" opertation.
			ctrlz_status = commands.getoutput("ssh "+group_name+"@"+server_ip+" -p "+server_port+"\
				'if [ -f ctrlz.txt  ];     \
				then echo \"existent\"; else echo \"nonexistent\" ; fi ; ' ")
			if ctrlz_status == "existent":
				download_ctrlz_txt = commands.getstatusoutput("scp -o StrictHostKeyChecking=no -P "+server_port+
					" "+group_name+"@"+server_ip+":ctrlz.txt /root/freeBSD_Files/")

				# This code is going to search the client's IP in order to know if a change is required
				with open("/root/freeBSD_Files/my_ip.txt", "r") as my_ip:
					ip_to_find = my_ip.read()
				
				with open("/root/freeBSD_Files/ctrlz.txt", "r") as ctrlz_txt:
					all_txt = ctrlz_txt.read()
					ctrlz_txt.seek(0)
					end_aux = 0
					the_begin = ""
					start_aux = 0
					ip_found_ctrlz = False
					for line in ctrlz_txt:
						end_aux += len(line)
						if line[:-1] == ip_to_find:
							start_aux = end_aux - len(line)
							ip_found_ctrlz = True
							break
						the_begin += line
					ctrlz_txt.seek(end_aux)
					the_rest = ctrlz_txt.read()
					ctrlz_txt.seek(start_aux)
				with open("/root/freeBSD_Files/ctrlz.txt", "w") as ctrlz_txt:
					ctrlz_txt.write(the_begin)
					ctrlz_txt.write(the_rest)
				
				if ip_found_ctrlz:
					print("CTRL Z IS NEEDED")
					backup_file = os.path.isfile("/backupCentralizedConsole/conf.xml")
					if backup_file:
						restore_backup = commands.getoutput("rm -f /cf/conf/config.xml ")
						restore_backup = commands.getoutput("cp /backupCentralizedConsole/cfconf.xml /cf/conf/config.xml ")
						restore_backup = commands.getoutput("rm -f /conf/config.xml ")
						restore_backup = commands.getoutput("cp /backupCentralizedConsole/conf.xml /conf/config.xml ")
						restore_backup = commands.getoutput("rm -f /tmp/config.cache")
						print("CTRLZ Z APPLIED")
						upload_ctrlz_txt = commands.getstatusoutput("scp -o StrictHostKeyChecking=no -P "+server_port+
							" /root/freeBSD_Files/ctrlz.txt "+group_name+"@"+server_ip+": ")
						print("CTRLZ TXT HAS BEEN UPDATED")
						delete_ctrlz_txt = commands.getoutput("rm -f /root/freeBSD_Files/ctrlz.txt")

					else: 
						print("IT WAS NOT POSSIBLE TO DO THE CTRL Z OPERATION. THERE IS NO BACKUP")

			elif ctrlz_status == "nonexistent":
				print("IT DOESNOT NEED CTRL Z")
			else: 
				print("It was not possible to connect with the server")
				print("Status: " + ctrlz_status)

			xml_status = commands.getoutput("ssh "+group_name+"@"+server_ip+" -p "+server_port+"\
				'if [ -f conf.xml  ];     \
				then echo \"existent\"; else echo \"nonexistent\" ; fi ; ' ")
			
			if xml_status == "existent":					
				print("XML EXISTS")
				ips_to_change = True
				while ips_to_change:


					ips_to_change = commands.getoutput("ssh "+group_name+"@"+server_ip+" -p "+server_port+"\
						'if [ -f /home/"+group_name+"/ips_to_change.txt  ];     \
						then echo \"existent\"; else echo \"nonexistent\" ; fi ; ' ")		

					if ips_to_change == "existent":
						print("TXT EXISTS")
						download_txt = commands.getstatusoutput("scp -o StrictHostKeyChecking=no -P "+server_port+
							" "+group_name+"@"+server_ip+":ips_to_change.txt /root/freeBSD_Files/")
						# delete_txt = commands.getstatusoutput("ssh "+group_name+"@"+server_ip+" -p "+server_port+" \
						# 	'rm -f ips_to_change.txt ; ' ")

						if download_txt[0] != 0:
							print("It was not possible to download the file")
						else: # TXT was downloaded
							print("TXT DOWNLOADED")
							ips_to_change = False
							
							# This code is going to search the client's IP in order to know if a change is required
							with open("/root/freeBSD_Files/my_ip.txt", "r") as my_ip:
								ip_to_find = my_ip.read()
							with open("/root/freeBSD_Files/ips_to_change.txt", "r") as ips_to_change:
								all_txt = ips_to_change.read()
								ips_to_change.seek(0)
								end_aux = 0
								the_begin = ""
								start_aux = 0
								ip_found = False
								for line in ips_to_change:
									end_aux += len(line)
									if line[:-1] == ip_to_find:
										start_aux = end_aux - len(line)
										ip_found = True
										break
									the_begin += line
								ips_to_change.seek(end_aux)
								the_rest = ips_to_change.read()
								ips_to_change.seek(start_aux)

							with open("/root/freeBSD_Files/ips_to_change.txt", "w") as ips_to_change:
								ips_to_change.write(the_begin)
								ips_to_change.write(the_rest)

							empty_txt = False
							with open("/root/freeBSD_Files/ips_to_change.txt", "r") as ips_to_change:
								all_txt = ips_to_change.read()
								if all_txt == "":
									empty_txt = True

							if ip_found:
								# It generates a backup.
								print("IP FOUND")

								backup_dir = os.path.isdir("/backupCentralizedConsole")
								if backup_dir:
									pass
								else:
									os.makedirs("/backupCentralizedConsole")
								backup = commands.getstatusoutput("cp /cf/conf/config.xml /backupCentralizedConsole/cfconf.xml")
								backup = commands.getstatusoutput("cp /conf/config.xml /backupCentralizedConsole/conf.xml")

								change_to_do_status = commands.getoutput("ssh "+group_name+"@"+server_ip+" -p "+server_port+"\
									'if [ -f change_to_do.txt  ];     \
									then echo \"existent\"; else echo \"nonexistent\" ; fi ; ' ")

								if change_to_do_status == "existent":
									# Here the change will be applied
									download_change_to_do = commands.getstatusoutput("scp -o StrictHostKeyChecking=no -P "+server_port+
										" "+group_name+"@"+server_ip+":change_to_do.txt /root/freeBSD_Files/")
									print("CHANGE TO DO DOWNLOADED")
									download_xml = commands.getstatusoutput("scp -o StrictHostKeyChecking=no -P "+server_port+
										" "+group_name+"@"+server_ip+":conf.xml /root/freeBSD_Files/applyChanges/")
									print("XML DOWNLOADED")
									with open("/root/freeBSD_Files/change_to_do.txt") as change_to_do_txt:
										change_to_do = change_to_do_txt.read()

									changesApplied = commands.getoutput("python2 /root/freeBSD_Files/applyChanges/"+change_to_do[:-1])
									print(changesApplied, " ")
									print("CHANGES HAS BEEN APPLIED")
									delete_xml = commands.getstatusoutput("rm -f /root/freeBSD_Files/applyChanges/conf.xml")
									delete_change_to_do = commands.getstatusoutput("rm -f /root/freeBSD_Files/change_to_do.txt")


									if empty_txt:
										delete_txt = commands.getstatusoutput("ssh "+group_name+"@"+server_ip+" -p "+server_port+" \
										 	'rm -f ips_to_change.txt ; ' ")
										print("TXT HAS BEEN ELIMINATED")
										delete_xml = commands.getstatusoutput("ssh "+group_name+"@"+server_ip+" -p "+server_port+" \
										 	'rm -f conf.xml ; ' ")
										print("XML HAS BEEN ELIMINATED")
									else:
										# Send to the server the new txt
										upload_txt = commands.getstatusoutput("scp -o StrictHostKeyChecking=no -P "+server_port+
											" /root/freeBSD_Files/ips_to_change.txt "+group_name+"@"+server_ip+": ")
										print("TXT HAS BEEN UPDATED")
									break
								elif change_to_do_status == "nonexistent":
									print("NOT POSSIBLE TO APLLY CHANGES. CHANGE_TO_DO_TXT DOESNOT EXISTS")
								else:
									print("Connection error:\nStatus: " + change_to_do_status)
							else:
								print("IP DOESNOT FOUND")
							delete_txt = commands.getstatusoutput("rm -f /root/freeBSD_Files/ips_to_change.txt")
							break
					elif ips_to_change == "nonexistent":
						print("TXT DOES NOT EXISTS")
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