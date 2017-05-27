#! /usr/bin/env python3

'''
Script to check access to the server, and if the existence of specific words in the html
content of a page that indicate probable defacement

Creation date: 24/01/2017
Date last updated: 19/03/2017

* 
* License: GPL
* Copyright (c) 2017 DI-FCUL
* 
* Description:
* 
* This file contains the check_defacement plugin
* 
* Use the nrpe program to check request on remote server.
* 
* 
* This program is free software: you can redistribute it and/or modify
* it under the terms of the GNU General Public License as published by
* the Free Software Foundation, either version 3 of the License, or
* (at your option) any later version.
* 
* You should have received a copy of the GNU General Public License
* along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

import os
import sys
from optparse import OptionParser
import urllib.request
import re
import urllib

__author__ = "\nAuthor: Raimundo Henrique da Silva Chipongue\nE-mail: fc48807@alunos.fc.ul.pt, chipongue1@gmail.com\nInstitution: Faculty of Science of the University of Lisbon\n"
__version__= "1.0.0"

# define exit codes
ExitOK = 0
ExitWarning = 1
ExitCritical = 2
ExitUnknown = 3

def verify(opts):   
    Ignore = []
    if opts.Ignore:
        Ig = [i for i in opts.Ignore.split(",")]
        Ignore.extend([i for i in Ig])
        Ignore = sorted(list(set(Ignore)))
    try:
        req = urllib.request.Request(opts.url)
        resp = urllib.request.urlopen(req,timeout=2)        
    except:
        print("Internet error or page not found, error 404, url: %s"%opts.url)
        sys.exit(ExitUnknown)

    path_tmp = opts.path
    if opts.ignore:
        keywords = []
    else:
        keywords = ['Anonymous','Hacked','Hacker','hack','h4ck3d',
                    'attack','Hacktivist','virus','defaced',
                    'Gary McKinnon','LulzSec','Lulz Security','lulz',
                    'Adrian Lamo','Astra','MafiaBoy','YTCracker','414s',
                    'FinnSec Security','Chaos Computer Club','Cicada 3301',
                    'Croatian Revolution Hackers','Cult of the Dead Cow',
                    'cDc','Decocidio','#Ө','Digital DawgPound','Global kOS ',
                    'globalHell','Goatse Security','GoatSec','Hacking Team',
                    'Hacking','Hackweiser','Honker Union','L0pht','Mazafaka',
                    'milw0rm','NCPH','OurMine','Syrian Electronic Army',
                    'TeaMp0isoN','UGNazi','bl@ck dr@gon','Lizard Squad',
                    'Tarh Andishan','ArabAttack','k4zuk3','kdms team',
                    'Dragonfly']
    
    if opts.keyword:
        newitem = [i for i in opts.keyword.split(",")]
        keywords.extend([i for i in newitem])
        keywords = sorted(list(set(keywords)))
    else:
        keywords = (sorted(keywords))
    try:
        os.popen("wget %s -O %sdefacement.html > /dev/null 2>&1"%(opts.url, path_tmp)).read()    
    except:
        print("Unable to connect")
        sys.exit(ExitUnknown)
    if os.path.exists("%sdefacement.html"%path_tmp):
        if not os.stat("%sdefacement.html"%path_tmp).st_size:
            print("Can't read the url: %s"%opts.url)
            sys.exit(ExitUnknown)
    else:
        print("Can't read the url: %s"%opts.url)
        sys.exit(ExitUnknown)
        
    keywords = sorted(list(set(keywords) - set(Ignore)))

    path = ("%sdefacement.html"%path_tmp)    
    word_macth = [] 
    num = 0
    for i in range(0,len(keywords)):   
        text = str(keywords[num])
        macth = int(os.popen("grep -i '%s' %s | wc -l"%(text, path)).read())        
        num = num +1
        if macth != 0:
            word_macth.extend([text])

    os.popen("rm -fr %sdefacement.html"%path_tmp).read()

    if word_macth != []:
        print('Dangerous words were found, verify that the following %s words "%s", are legitimate in the following web page: %s'%(len(word_macth),(", ".join(word_macth)),opts.url))
        sys.exit(ExitCritical)  
    else:
        print("No dangerous words are found")
        sys.exit(ExitOK)
                  
def main():
    parser = OptionParser("usage: %prog [options] ARG1 ARG2 FOR EXAMPLE: -U https://www.ciencias.ulisboa.pt -K hacker,hacked,anonymous")
    parser.add_option("-U","--url", dest="url",
                      help="Specify the full url you want to check, i.e. -U https://www.ciencias.ulisboa.pt")
    parser.add_option("-K","--keyword", dest="keyword", default=False,
                      help="Put the words you want to search, i.e. -K hacker,hacked,anonymous")
    parser.add_option("-V","--version", action="store_true", dest="version", help="This option show the current version number of the program and exit")
    parser.add_option("-A","--author", action="store_true", dest="author", help="This option show author information and exit")
    parser.add_option("-i","--ignore", action="store_true", dest="ignore",
                      help="Use this option to ignore all pre-installed suspect words")
    parser.add_option("-I","--Ignore", dest="Ignore",default=False, type=str,
                      help="Use this option to ignore one or multiple pre-installed suspect words")
    parser.add_option("-p","--path", dest="path", default="/tmp/",
                      help="Specify the full path of the folder where you store temp file." +
                      "By default this is /tmp/ folder")
    (opts, args) = parser.parse_args()
    
    if opts.author:
        print(__author__)
        sys.exit()
    if opts.version:
        print("check_defacement.py %s"%__version__)
        sys.exit()
    if opts.ignore:
        if not opts.keyword:
            parser.error("When using -i option, you need to specify at least one suspect word.")
    if opts.url:
        verify(opts)
    else:
        parser.error("Please, this program requires url arguments.")  

if __name__ == '__main__':
    main()
