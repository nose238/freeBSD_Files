#!/usr/bin/env python
# -*- coding: utf-8 -*-

################################################################
# This Code Has Been Developed By                              #
# Jozic Espinoza  -- AKA HackeMatte                            #
# Eduardo Marquez -- nose238@hotmail.com                       #
################################################################
import os


os.system("cp /cf/conf/config.xml /root/freeBSD_Files/applyChanges/")
# Extra code... verify if aliases tags are in the format required.
configXML = open("/root/freeBSD_Files/applyChanges/config.xml", "r+")
lines = len(  list(  open("/root/freeBSD_Files/applyChanges/config.xml", "r+")    )   )
numberline = 0
for line in configXML:
    numberline += 1
    if "<separator>" in line:
        break
    elif numberline == lines:
        file =  open("/root/freeBSD_Files/applyChanges/config.xml", "r+")
        number = 0
        for l in file:
            if "</filter>" in l:
                file.seek(number)
                string = file.readlines()
                file.seek(number)
                file.write("\t\t<separator>\n\t\t\t<wan></wan>\n\t\t\t<lan></lan>\n\t\t</separator>\n")
                for otherline in string:
                    file.write(otherline)
                break
            number += len(l)
        file.close()
        break
configXML.close()

#####Start variables section#####
Sq=0      #squid
Sq1=0     #squid1
Sq2=0     #squid2
Sq3=0     #squid3
Sq4=0     #squid4
SqA=0     #squidA
SqA1=0    #squidA1
SqA2=0    #squidA2
SqA3=0    #squidA3
SqA4=0    #squidA4
Sqg=0     #squidg
Sqg1=0    #squidg1
Sqg2=0    #squidg2
Sqg3=0    #squidg3
Sqg4=0    #squidg4
#####End variables section#####

#####Start XML labels section#####
#Words to search, it means, the xml labels for squid
label="<filter>"                   #Start label for firewall rules
label1="</filter>"                 #End label for firewall
labelA="<filter>"                  #Start label for firewall rules
labelA1="</filter>"                #End label for firewall

####SquidGuard Section####
labelsq="<?xml version=\"1.0\"?>"  #Start label for XMLconfiguration file
label1sq="<filter>"                #Start firewall label
label2sq="</filter>"               #Start firewall label
label3sq="</pfsense>"             #End label for XML configuration file

####Aux variables for increase the counter####
auxLabel="<separator>"
#####End XML labels section#####

####Start user section####
#read the Xml User file

with open("/root/freeBSD_Files/applyChanges/config.xml") as f:
    for line in f:
        Sq1 += 1
        if label in line:
            squid1 = (Sq1+1)
with open("/root/freeBSD_Files/applyChanges/config.xml") as f:
    for line in f:
        Sq2 += 1
        if auxLabel in line and Sq2 > squid1:
            squid2 = (Sq2-1)

#command for cut an interval of speciffic lines and create a new file with those lines
#Firewall rules user doc
command1  = 'sed \''+str(squid1)+','+str(squid2)+' !d\' /root/freeBSD_Files/applyChanges/config.xml > /root/freeBSD_Files/applyChanges/rulesUser.xml'
os.system(command1)
####End user section####

####Start the admin section####
#read the Xml Admin file
with open("/root/freeBSD_Files/applyChanges/conf.xml") as f:
    for line in f:
        SqA += 1
        if labelA in line:
            squidA = (SqA+1)
with open("/root/freeBSD_Files/applyChanges/conf.xml") as f:
    for line in f:
        SqA1 += 1
        if labelA1 in line:
            squidA1 = (SqA1)
with open("/root/freeBSD_Files/applyChanges/conf.xml") as f:
    for line in f:
        SqA2 += 1
        if auxLabel in line and SqA2 < squidA1:
            squidA2 = (SqA2-1)

#command for cut an interval of speciffic lines and create a new file with those lines
#Firewall rules admin doc
commandA1  = 'sed \''+str(squidA)+','+str(squidA2)+' !d\' /root/freeBSD_Files/applyChanges/conf.xml > /root/freeBSD_Files/applyChanges/rulesAdmin.xml'
os.system(commandA1)
####End admin section####

####Start merge Section####
commandMix1 = 'cat /root/freeBSD_Files/applyChanges/rulesUser.xml /root/freeBSD_Files/applyChanges/rulesAdmin.xml > /root/freeBSD_Files/applyChanges/finalRules.xml'
commandremoveU1 = 'rm -r -f /root/freeBSD_Files/applyChanges/rulesUser.xml'
commandremoveA1 = 'rm -r -f /root/freeBSD_Files/applyChanges/rulesAdmin.xml'
os.system(commandMix1)
os.system(commandremoveU1)
os.system(commandremoveA1)

#####Start get final document section#####
with open("/root/freeBSD_Files/applyChanges/config.xml") as f:
    for line in f:
        Sqg += 1
        if labelsq in line:
            squidg = (Sqg)
with open("/root/freeBSD_Files/applyChanges/config.xml") as f:
    for line in f:
        Sqg1 += 1
        if label1sq in line:
            squidg1 = (Sqg1)
with open("/root/freeBSD_Files/applyChanges/config.xml") as f:
    for line in f:
        Sqg2 += 1
        if label2sq in line:
            squidg2 = (Sqg2)
with open("/root/freeBSD_Files/applyChanges/config.xml") as f:
    for line in f:
        Sqg3 += 1
        if auxLabel in line and Sqg3 < squidg2:
            squidg3 = (Sqg3)
with open("/root/freeBSD_Files/applyChanges/config.xml") as f:
    for line in f:
        Sqg4 += 1
        if label3sq in line:
            squidg4 = (Sqg4)

#command for cut an interval of speciffic lines and create a new file with those lines
#before Firewall Rules doc
commandsq1  = 'sed \''+str(squidg)+','+str(squidg1)+' !d\' /root/freeBSD_Files/applyChanges/config.xml > /root/freeBSD_Files/applyChanges/beforeRules.xml'
os.system(commandsq1)
#before Aliases doc
commandsq2  = 'sed \''+str(squidg3)+','+str(squidg4)+' !d\' /root/freeBSD_Files/applyChanges/config.xml > /root/freeBSD_Files/applyChanges/beforeEnd.xml'
os.system(commandsq2)
####get final document section####

###Start semifinal merge Section####
commandMixsq1 = 'cat /root/freeBSD_Files/applyChanges/beforeRules.xml /root/freeBSD_Files/applyChanges/finalRules.xml > /root/freeBSD_Files/applyChanges/finalsq1.xml'
commandremovesq1 = 'rm -r -f /root/freeBSD_Files/applyChanges/beforeRules.xml'
commandremovesqg1 = 'rm -r -f /root/freeBSD_Files/applyChanges/finalRules.xml'
os.system(commandMixsq1)
os.system(commandremovesq1)
os.system(commandremovesqg1)
commandMixsq2 = 'cat /root/freeBSD_Files/applyChanges/finalsq1.xml /root/freeBSD_Files/applyChanges/beforeEnd.xml > /root/freeBSD_Files/applyChanges/finalsq2.xml'
commandremovesq2 = 'rm -r -f /root/freeBSD_Files/applyChanges/beforeEnd.xml'
commandremovesqg2 = 'rm -r -f /root/freeBSD_Files/applyChanges/finalsq1.xml'
os.system(commandMixsq2)
os.system(commandremovesq2)
os.system(commandremovesqg2)
####End semifinal merge section####

####Start the final section####
commandDelete1 = 'rm -r -f /root/freeBSD_Files/applyChanges/conf.xml'
commandDelete2 = 'rm -r -f /root/freeBSD_Files/applyChanges/config.xml'
commandDelete3 = 'mv /root/freeBSD_Files/applyChanges/finalsq2.xml /root/freeBSD_Files/applyChanges/config.xml'
os.system(commandDelete1)
os.system(commandDelete2)
os.system(commandDelete3)
####End the final section####

#apply changes and delete cache
os.system("rm -f /cf/conf/config.xml")
os.system("mv /root/freeBSD_Files/applyChanges/config.xml /cf/conf/config.xml")
os.system("rm -f /tmp/config.cache")
