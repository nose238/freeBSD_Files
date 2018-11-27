confXML = open("conf.xml", "r")

number = 0
#!/usr/bin/env python
# -*- coding: utf-8 -*-

################################################################
# This Code Has Been Developed By                              #
# Eduardo Marquez -- nose238@hotmail.com                       #
################################################################
import os
os.system("cp /cf/conf/config.xml /root/freeBSD_Files/applyChanges/")

for line in confXML:
    number += len(line)
    if "<nat>" in line:
        otherDoc = open("conf.xml", "r")
        otherDoc.seek(number)
        to_add = otherDoc.read()
        otherDoc.close()
        break
confXML.close()

configXML = open("config.xml", "r+")

number = 0
for line in configXML:
    number += len(line)
    if "</nat>" in line:
        rest = open("config.xml", "r+")
        rest.seek(number)
        string = rest.read()
        rest.close()
        configXML.seek(number - len("\t\t</nat>\n") )
        configXML.write("\n" + to_add  + "\n" + string)
        break
configXML.close()


#apply changes and delete cache
os.system("rm -f /cf/conf/config.xml")
os.system("mv config.xml /cf/conf/config.xml")
os.system("rm -f /tmp/config.cache")