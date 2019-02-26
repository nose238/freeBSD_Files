#!/usr/bin/env python
# -*- coding: utf-8 -*-

################################################################
# This Code Has Been Developed By                              #
# Jozic Espinoza  -- AKA HackeMatte                            #
#E duardo Marquez -- nose238@hotmail.com                       #
################################################################
import os


os.system("cp /cf/conf/config.xml /root/freeBSD_Files/applyChanges/")
# Extra code... verify if aliases tags are in the format required.
f = open("/root/freeBSD_Files/applyChanges/config.xml", "r+")
numberline = 0
for line in f:
    numberline += len(line)
    if "<aliases></aliases>" in line:
        f.seek(numberline-len("</aliases>")-1)
        string = f.readlines()
        f.seek(numberline-len("</aliases>")-1)
        f.write("\n\n\t")
        for other_line in string:
            f.write(other_line)
        f.close()
        break
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
label="<aliases>"                   #Start label for aliases
label1="</aliases>"                 #End label for aliases
labelA="<aliases>"                  #Start label for aliases
labelA1="</aliases>"                #End label for aliases

####SquidGuard Section####
labelsq="<?xml version=\"1.0\"?>" #Start label for XMLconfiguration file
label1sq="<aliases>"              #Start aliases label
label2sq="</aliases>"             #Start aliases label
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
        if label1 in line:
            squid2 = (Sq2-1)

#command for cut an interval of speciffic lines and create a new file with those lines
#Aliases user doc
command1  = 'sed \''+str(squid1)+','+str(squid2)+' !d\' /root/freeBSD_Files/applyChanges/config.xml > /root/freeBSD_Files/applyChanges/aliasesUser.xml'
os.system(command1)
####End the user section####

####Start the admin section####
#read the Xml admin file
with open("/root/freeBSD_Files/applyChanges/conf.xml") as f:
    for line in f:
        SqA += 1
        if labelA in line:
            squidA = (SqA+1)
with open("/root/freeBSD_Files/applyChanges/conf.xml") as f:
    for line in f:
        SqA1 += 1
        if labelA1 in line:
            squidA1 = (SqA1-1)

#command for cut an interval of speciffic lines and create a new file with those lines
#Aliases admin doc
commandA1  = 'sed \''+str(squidA)+','+str(squidA1)+' !d\' /root/freeBSD_Files/applyChanges/conf.xml > /root/freeBSD_Files/applyChanges/aliasesAdmin.xml'
os.system(commandA1)
#####End admin section#####

####Start merge Section####
commandMix1 = 'cat /root/freeBSD_Files/applyChanges/aliasesUser.xml /root/freeBSD_Files/applyChanges/aliasesAdmin.xml > /root/freeBSD_Files/applyChanges/finalAliases.xml'
commandremoveU1 = 'rm -r -f /root/freeBSD_Files/applyChanges/aliasesUser.xml'
commandremoveA1 = 'rm -r -f /root/freeBSD_Files/applyChanges/aliasesAdmin.xml'
os.system(commandMix1)
os.system(commandremoveU1)
os.system(commandremoveA1)
#####End merge section#####

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
        if label3sq in line:
            squidg3 = (Sqg3)

#command for cut an interval of speciffic lines and create a new file with those lines
#before Aliases doc
commandsq1  = 'sed \''+str(squidg)+','+str(squidg1)+' !d\' /root/freeBSD_Files/applyChanges/config.xml > /root/freeBSD_Files/applyChanges/beforeAliases.xml'
os.system(commandsq1)
#before Aliases doc
commandsq2  = 'sed \''+str(squidg2)+','+str(squidg3)+' !d\' /root/freeBSD_Files/applyChanges/config.xml > /root/freeBSD_Files/applyChanges/beforeEnd.xml'
os.system(commandsq2)
#####End get final document section#####

####Start semifinal merge Section####
commandMixsq1 = 'cat /root/freeBSD_Files/applyChanges/beforeAliases.xml /root/freeBSD_Files/applyChanges/finalAliases.xml > /root/freeBSD_Files/applyChanges/finalsq1.xml'
commandremovesq1 = 'rm -r -f /root/freeBSD_Files/applyChanges/beforeAliases.xml'
commandremovesqg1 = 'rm -r -f /root/freeBSD_Files/applyChanges/finalAliases.xml'
os.system(commandMixsq1)
os.system(commandremovesq1)
os.system(commandremovesqg1)
commandMixsq2 = 'cat /root/freeBSD_Files/applyChanges/finalsq1.xml /root/freeBSD_Files/applyChanges/beforeEnd.xml > /root/freeBSD_Files/applyChanges/finalsq2.xml'
commandremovesq2 = 'rm -r -f /root/freeBSD_Files/applyChanges/finalsq1.xml'
commandremovesqg2 = 'rm -r -f /root/freeBSD_Files/applyChanges/beforeEnd.xml'
os.system(commandMixsq2)
os.system(commandremovesq2)
os.system(commandremovesqg2)
#####End semifinal merge section#####

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
