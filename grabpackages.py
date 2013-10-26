#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
:Version: 0.1
:Author: Sergio de la Cruz Rodríguez.
:Organization: Cinvestav Unidad Guadalajara. Jalisco. Mexico
:Contact: scruz@gdl.cinvestav.mx
:Copyright: © 2009. All rights reserved.
:License: GPLv3

Grabs packages needed to install an application in Debian-like linux distributions.
'''

import sys
import os
import re
import commands
import locale
import pickle
from optparse import OptionParser

# This string is the pickled version of a locale table that stores translations for the word 'Depends'
locales_dict = "(dp0\nS'el'\np1\nS'\\xce\\x95\\xce\\xbe\\xce\\xb1\\xcf\\x81\\xcf\\x84\\xce\\xac\\xcf\\x84\\xce\\xb1\\xce\\xb9 \\xce\\xb1\\xcf\\x80\\xcf\\x8c'\np2\nsS'mr'\np3\nS'\\xe0\\xa4\\x85\\xe0\\xa4\\xb5\\xe0\\xa4\\xb2\\xe0\\xa4\\x82\\xe0\\xa4\\xac\\xe0\\xa4\\xbf\\xe0\\xa4\\xa4'\np4\nsS'vi'\np5\nS'Ph\\xe1\\xbb\\xa5 thu\\xe1\\xbb\\x99c'\np6\nsS'ca'\np7\nS'Dep\\xc3\\xa9n'\np8\nsS'it'\np9\nS'Dipende'\np10\nsS'cs'\np11\nS'Z\\xc3\\xa1vis\\xc3\\xad na'\np12\nsS'cy'\np13\nS'Dibynnu'\np14\nsS'ar'\np15\nS'\\xd9\\x8a\\xd8\\xb9\\xd8\\xaa\\xd9\\x85\\xd8\\xaf'\np16\nsS'bg'\np17\nS'\\xd0\\x97\\xd0\\xb0\\xd0\\xb2\\xd0\\xb8\\xd1\\x81\\xd0\\xb8 \\xd0\\xbe\\xd1\\x82'\np18\nsS'eu'\np19\nS'Mendekotasuna:'\np20\nsS'gl'\np21\nS'Depende'\np22\nsS'es'\np23\nS'Depende'\np24\nsS'ru'\np25\nS'\\xd0\\x97\\xd0\\xb0\\xd0\\xb2\\xd0\\xb8\\xd1\\x81\\xd0\\xb8\\xd1\\x82'\np26\nsS'nl'\np27\nS'Vereisten'\np28\nsS'pt'\np29\nS'Depende'\np30\nsS'nb'\np31\nS'Avhenger av'\np32\nsS'ne'\np33\nS'\\xe0\\xa4\\x86\\xe0\\xa4\\xa7\\xe0\\xa4\\xbe\\xe0\\xa4\\xb0\\xe0\\xa4\\xbf\\xe0\\xa4\\xa4'\np34\nsS'tl'\np35\nS'Dependensiya'\np36\nsS'th'\np37\nS'\\xe0\\xb8\\x95\\xe0\\xb9\\x89\\xe0\\xb8\\xad\\xe0\\xb8\\x87\\xe0\\xb9\\x83\\xe0\\xb8\\x8a\\xe0\\xb9\\x89'\np38\nsS'ro'\np39\nS'Depinde'\np40\nsS'pl'\np41\nS'Wymaga'\np42\nsS'fr'\np43\nS'D\\xc3\\xa9pend'\np44\nsS'de'\np45\nS'H\\xc3\\xa4ngt ab'\np46\nsS'uk'\np47\nS'\\xd0\\x97\\xd0\\xb0\\xd0\\xbb\\xd0\\xb5\\xd0\\xb6\\xd0\\xbd\\xd0\\xbe\\xd1\\x81\\xd1\\x82\\xd1\\x96 (Depends)'\np48\nsS'pt_BR'\np49\nS'Depende'\np50\nsS'zh_TW'\np51\nS'\\xe4\\xbe\\x9d\\xe5\\xad\\x98\\xe9\\x97\\x9c\\xe4\\xbf\\x82'\np52\nsS'da'\np53\nS'Afh\\xe6ngigheder'\np54\nsS'dz'\np55\nS'\\xe0\\xbd\\xa2\\xe0\\xbe\\x9f\\xe0\\xbd\\xba\\xe0\\xbd\\x93\\xe0\\xbd\\x98\\xe0\\xbc\\x8b\\xe0\\xbd\\xa8\\xe0\\xbd\\xb2\\xe0\\xbd\\x93\\xe0\\xbc\\x8d'\np56\nsS'bs'\np57\nS'Zavisi'\np58\nsS'fi'\np59\nS'Riippuvuudet'\np60\nsS'hu'\np61\nS'F\\xc3\\xbcgg ett\\xc5\\x91l'\np62\nsS'ja'\np63\nS'\\xe4\\xbe\\x9d\\xe5\\xad\\x98'\np64\nsS'he'\np65\nS''\np66\nsS'nn'\np67\nS'Krav'\np68\nsS'zh_CN'\np69\nS'\\xe4\\xbe\\x9d\\xe8\\xb5\\x96'\np70\nsS'ko'\np71\nS'\\xec\\x9d\\x98\\xec\\xa1\\xb4'\np72\nsS'sv'\np73\nS'Beroende av'\np74\nsS'km'\np75\nS'\\xe1\\x9e\\xa2\\xe1\\x9e\\xb6\\xe1\\x9e\\x9f\\xe1\\x9f\\x92\\xe1\\x9e\\x9a\\xe1\\x9f\\x90\\xe1\\x9e\\x99\\xe2\\x80\\x8b'\np76\nsS'sk'\np77\nS'Z\\xc3\\xa1vis\\xc3\\xad na'\np78\nsS'en_GB'\np79\nS'Depends'\np80\nsS'ku'\np81\nS'Bindest'\np82\nsS'sl'\np83\nS'Odvisen od'\np84\ns."

def deps(pkgs):
    ''' 
    Generates a list containing the names of the packages needed to install the given package(s)
    Takes a list of the desired packages as a parameter.
    '''
    loc = pickle.loads(locales_dict)
    lang = locale.getdefaultlocale()[0] # Returns something like 'es_MX'
    depstr = loc.get(lang) or loc.get(lang[:2]) or 'Depends'
    regex = re.compile('^\s*' + depstr +': (.*?)$', re.M | re.U)
    ready = set(pkgs)
    for item in pkgs:
        ready.update(regex.findall(commands.getoutput('apt-cache -i --recurse depends '+item)))
    return ready.intersection([item for item in ready if not (item.startswith('<') and item.endswith('>'))])



def get_debs(pkgs,  repo,  check):
    ''' 
    Generates a dictionary to store the URLs of the given packages.
    The keys of the dictionary are the package names and the values are their corresponding URLs.
    Takes a list of the desired packages as a parameter.
    '''
    loc = pickle.loads(locales_dict)
    res = {}
    archive = set(os.listdir('/var/cache/apt/archives'))
    for item in deps(pkgs):
        description = commands.getoutput('apt-cache show ' + item)
        try:
            uri = re.search(r'^Filename: (.*?)$',description, re.M).groups()[0]
        except: continue
        if check:
            name = uri[uri.rfind('/')+1:]   # only the name and the extension
            if name in archive: continue
        res[item] = repo + uri
    return res
    



if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("--html", 
                    action='store_true', dest="htmloutput", default=False, 
                    help="Write output links in html format (so you can download them with something like DownThemAll")
    parser.add_option("-o", "--output-file",
                  action="store", type="string", dest="ofile",  default='', 
                  help = 'Name of the file to write the results to')
    parser.add_option("-r", "--repository",
                  action="store", type="string", dest="repo",  default='http://archive.ubuntu.com/ubuntu/', 
                  help = 'Repository to use. Defaults to "http://archive.ubuntu.com/ubuntu/"')
    parser.add_option("-c", "--check", 
                    action='store_true', dest="archivecheck", default=False, 
                    help="Generate download link only if the package is not already in the archive")

    (options, args) = parser.parse_args()

    if not args:
        print 'No package(s) to grab. Type "python grabpackages.py -h" to show help.'
        sys.exit()

    packages = get_debs(args, options.repo,  options.archivecheck)
    content = ('wget -c ' + " ".join(packages.values())) if not options.htmloutput else \
              "\n".join(["<a href='%s'>%s</a><br/>" % (value,key) for key,value in packages.iteritems()])
    fich = open(options.ofile, 'w') if options.ofile else sys.stdout
    fich.write(content)


