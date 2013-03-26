#! /bin/python

#contactsfile = "/home/jan/.wine/drive_c/users/jan/Local Settings/Application Data/Google/Picasa2/contacts/contacts.xml"
contactsfile = "/home/jan/Dokumente/Programmieren/pyFaceExtract/test/contacts.xml"

#System environment
import sys
import os
import ConfigParser
import string
#use pyexiftool
from lib.pyexiftool import exiftool

#Found here: https://sites.google.com/site/picasafacenetwork/home
#not tested yet
############################################################################
#
#   Function to read id tags and names stored in Picasa contacts.xml file.
#
############################################################################

def Contacts(contactsfile):

    file = open(contactsfile)

    Contactids = []
    Names = []
    Displaynames = []

    while 1:
        line = file.readline()
        cid = line.find("contact id")
        if cid > 0:
            nstart = line.find("name=")
            dispstart = line.find("display=")
            modstart = line.find("modified")         

            cid = line[cid+12:nstart-2]
            name = line[nstart+6:dispstart-2]
            dispname = line[dispstart+9:modstart-2]

            Contactids.append(cid)
            Names.append(name)
            Displaynames.append(dispname)

        if not line:
            break

    Contactinfo = [Contactids,Names,Displaynames]

    return Contactinfo

def createNameList(contactsfile):
    namelist={}
    file = open(contactsfile)

    while 1:
        line = file.readline()
        cid = line.find("contact id")
        if cid > 0:
            nstart = line.find("name=")
            nend = line.find("modified")

            cid = line[cid+12:nstart-2]
            name = line[nstart+6:nend-2]

            namelist[cid]=name
        if not line:
            break

    return namelist

#This function saves the names to the images (xmp:Name)
def writeNamesToFiles(imgs, path):
    directory = os.path.dirname(path)

    for item in imgs:
        filepath = os.path.join(directory, item)
        print filepath
        sep=", "
        names = sep.join(imgs[item])
        if len(names) > 0 :
            print names
    return


#MAIN
#path to picasa.ini should be an argument:
if len(sys.argv) > 1:
    path = sys.argv[1]
    
    #maybe we should check if the last part of path is 'picasa.ini'...
    if os.path.isfile(path):
        contactmap = createNameList(contactsfile)
        #found here: http://www.python-forum.org/pythonforum/viewtopic.php?f=3&t=22097&start=0#p100203
        config = ConfigParser.ConfigParser()
        config.read(path)
        #we will write all information in dictionary first:
        imgs = {}

        #loop over all images found in the .picasa.ini
        for item in config.sections():
            #create list entry for this image
            imgs[item]=[]

            
            #with exiftool.ExifTool() as et:
            #    metadata = et.get_metadata(filepath)
           
            #print metadata
            try:
                #take all faces detected in this image
                faces = config.get(item, 'faces').split(';')
                for f in faces:
                    face = f.split(',')[1]
                    try:
                        #and look for a name:
                        name = contactmap[face]
                        if face != "ffffffffffffffff":
                            #we found a (proper) name, so add it to the dictionary
                            print "Adding name '"+name+"' to file '"+item+"'"
                            imgs[item].append(name)
                        else:
                            #No name attached to the face (aka unkown face in picasa)
                            "Face not identified"
                    except:
                        #no name found for the face (not saved in the contatcs.xml)
                        print "No name found for this id"
                #lets see what we found:
                #print imgs
                #here we should write the names to the images
                writeNamesToFiles(imgs, path)
            except:
                print "No faces saved in this file ('"+item+"')"
    else:
        print "Please enter path to 'picasa.ini' as first argument"
        sys.exit(0)
else:
    print "Please enter path to 'picasa.ini' as first argument"
    sys.exit(0)
