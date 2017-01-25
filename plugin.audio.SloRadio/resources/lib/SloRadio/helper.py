import sys, os
import urllib, urllib2, urlparse, json
import xbmc, xbmcgui, xbmcplugin, xbmcaddon
import re

from SloRadio.logging import log, LOGLEVEL, log_error

__addon__ = xbmcaddon.Addon()
__addonname__ = __addon__.getAddonInfo('name')
__addondir__ = xbmc.translatePath(__addon__.getAddonInfo('profile'))

_ver_file = os.path.join(__addondir__, 'verFile.txt')
_ver_file2 = os.path.join(__addondir__, 'verFile2.txt')
_radios_file = os.path.join(__addondir__, 'radios.json')

url = 'https://raw.githubusercontent.com/markop159/SLO-Radio-Stations/master/media'

log("(helper) Url:%s" %url, LOGLEVEL.INFO)

def checkVer():
    # check if directory exists
    if not os.path.exists(__addondir__):
        os.makedirs(__addondir__)

    # check if file exists
    if not os.path.isfile(_ver_file):
        downloadFiles('all')

    downloadFiles('ver')
    f=open(_ver_file, 'r')
    f2=open(_ver_file2, 'r')
    a = f.read()
    b = f2.read()
    log("(helper) checkVer a:%s b:%s" % (a,b), LOGLEVEL.INFO)
    if a == b:
        pass
    else:
        try:
            downloadFiles('all')
        except:
            pass

def downloadFiles(files):
    if files == 'all':
        urllib.urlretrieve ("%s/verFile.txt" %url, '%sverFile.txt' %__addondir__)
        urllib.urlretrieve ("%s/radios.json" %url, '%sradios.json' %__addondir__)
    else:
        urllib.urlretrieve ("%s/verFile.txt" %url, '%sverFile2.txt' %__addondir__)

def loadJson(menu):
    with open(_radios_file) as radios_file:
        radios = json.load(radios_file)
        log("(helper) loadJson:%s" %radios, LOGLEVEL.INFO)

    return radios[menu]

def loadJson2(menu, submenu):
    with open(_radios_file) as radios_file:
        radios = json.load(radios_file)
        log("(helper) loadJson:%s" %radios, LOGLEVEL.INFO)

    for item in radios[menu]:
        if item['title'] == submenu:
            return item['sub']
