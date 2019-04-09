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
			tmp_file = open("/root/freeBSD_Files/dir_name.txt", "r")
			dir_name = tmp_file.read()
			tmp_file.close()
			print("It works! " + time.strftime("%c"))
			markups = ["interfaces", "aliases", "squidguardacl", "squidguarddest", "filter", "nat"]
			for markup in markups:
				print("TRYING TO GENERATE "+markup+" INFO")
				os.system("cp /cf/conf/config.xml /root/freeBSD_Files/")
				number = 0
				begin = 0
				with open("/root/freeBSD_Files/config.xml", "r") as confXML:
					markup_exists = False
					for line in confXML:
						if "<"+markup+">" in line:
							markup_exists = True
					confXML.seek(0)
					for line in confXML:
						number += len(line)
						if "<"+markup+">" in line and "</"+markup+">" in line:
							continue
						if "<"+markup+">" in line:
							begin = number-len(line)
							continue
						elif "</"+markup+">" in line:
							end = number
					confXML.seek(begin)
					if markup_exists:
						content = confXML.read(end-begin)
					else:
						content = "There is no info available. Maybe "+markup+" is not installed."
				os.system("rm -f /root/freeBSD_Files/config.xml")
				with open("/root/freeBSD_Files/info_"+markup+".xml", "w") as infoXML:
					infoXML.write(content)
				infoStatus = commands.getstatusoutput("scp -o StrictHostKeyChecking=no -P "+server_port+
					" /root/freeBSD_Files/info_"+markup+".xml "+group_name+"@"+server_ip+":xml/"+dir_name+"/ ")
				if infoStatus[0] != 0:
					print("SENDING INFO "+markup+" FAILED")
				else:
					print("INFO SENDED")
				os.system("rm -f /root/freeBSD_Files/info_"+markup+".xml")
			# Verify if we have to do a "ctrl + z" opertation.
			ctrlz_status = commands.getoutput("ssh "+group_name+"@"+server_ip+" -p "+server_port+"\
				'if [ -f xml/"+dir_name+"/ctrlz.txt  ];     \
				then echo \"existent\"; else echo \"nonexistent\" ; fi ; ' ")
			if ctrlz_status == "existent":
				print("CTRL Z IS NEEDED")

				backup_file = os.path.isfile("/backupCentralizedConsole/conf.xml")
				if backup_file:
					restore_backup = commands.getoutput("rm -f /cf/conf/config.xml ")
					restore_backup = commands.getoutput("cp /backupCentralizedConsole/cfconf.xml /cf/conf/config.xml ")
					restore_backup = commands.getoutput("rm -f /conf/config.xml ")
					restore_backup = commands.getoutput("cp /backupCentralizedConsole/conf.xml /conf/config.xml ")
					restore_backup = commands.getoutput("rm -f /tmp/config.cache")
					print("CTRLZ Z APPLIED")
					delete_ctrlz_txt = commands.getoutput("ssh "+group_name+"@"+server_ip+" -p "+server_port+"\
						'rm -f xml/"+dir_name+"/ctrlz.txt ' ")
				else: 
					print("IT WAS NOT POSSIBLE TO DO THE CTRL Z OPERATION. THERE IS NO BACKUP")
			elif ctrlz_status == "nonexistent":
				print("IT DOESNOT NEED CTRL Z")
			else: 
				print("It was not possible to connect with the server")
				print("Status: " + ctrlz_status)
			xml_status = commands.getoutput("ssh "+group_name+"@"+server_ip+" -p "+server_port+"\
				'if [ -f xml/"+dir_name+"/conf.xml  ];     \
				then echo \"existent\"; else echo \"nonexistent\" ; fi ; ' ")
			if xml_status == "existent":					
				print("XML EXISTS")
				backup_dir = os.path.isdir("/backupCentralizedConsole")
				if backup_dir:
					pass
				else:
					os.makedirs("/backupCentralizedConsole")
				backup = commands.getstatusoutput("cp /cf/conf/config.xml /backupCentralizedConsole/cfconf.xml")
				backup = commands.getstatusoutput("cp /conf/config.xml /backupCentralizedConsole/conf.xml")
				print("BACKUP IS GENERATED")
				change_to_do_status = commands.getoutput("ssh "+group_name+"@"+server_ip+" -p "+server_port+"\
					'if [ -f xml/"+dir_name+"/change_to_do.txt  ];     \
					then echo \"existent\"; else echo \"nonexistent\" ; fi ; ' ")
				if change_to_do_status == "existent":
					# Here the change will be applied
					download_change_to_do = commands.getstatusoutput("scp -o StrictHostKeyChecking=no -P "+server_port+
						" "+group_name+"@"+server_ip+":xml/"+dir_name+"/change_to_do.txt /root/freeBSD_Files/")
					print("CHANGE TO DO DOWNLOADED")
					download_xml = commands.getstatusoutput("scp -o StrictHostKeyChecking=no -P "+server_port+
						" "+group_name+"@"+server_ip+":xml/"+dir_name+"/conf.xml /root/freeBSD_Files/applyChanges/")
					print("XML DOWNLOADED")
					with open("/root/freeBSD_Files/change_to_do.txt") as change_to_do_txt:
						change_to_do = change_to_do_txt.read()
					changesApplied = commands.getoutput("python2 /root/freeBSD_Files/applyChanges/"+change_to_do[:-1])
					print(changesApplied, " ")
					print("CHANGES HAS BEEN APPLIED")
					delete_xml = commands.getstatusoutput("rm -f /root/freeBSD_Files/applyChanges/conf.xml")
					delete_change_to_do = commands.getstatusoutput("rm -f /root/freeBSD_Files/change_to_do.txt")
					delete_txt = commands.getstatusoutput("ssh "+group_name+"@"+server_ip+" -p "+server_port+" \
					 	'rm -f xml/"+dir_name+"/change_to_do.txt ; ' ")
					print("CHANGE_TO_DO HAS BEEN ELIMINATED")
					delete_xml = commands.getstatusoutput("ssh "+group_name+"@"+server_ip+" -p "+server_port+" \
					 	'rm -f xml/"+dir_name+"/conf.xml ; ' ")
					print("XML HAS BEEN ELIMINATED")
				elif change_to_do_status == "nonexistent":
					print("NOT POSSIBLE TO APLLY CHANGES. CHANGE_TO_DO_TXT DOESNOT EXISTS")
				else:
					print("Connection error:\nStatus: " + change_to_do_status)
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