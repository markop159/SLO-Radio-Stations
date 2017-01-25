import sys, os
import urllib, urllib2, urlparse, json
import xbmcgui, xbmcplugin, xbmcaddon
import re

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'resources', 'lib'))
__addon__ = xbmcaddon.Addon()

from SloRadio.helper import loadJson, loadJson2, checkVer
from SloRadio.logging import log, LOGLEVEL, log_error

base = str(sys.argv[0])

def main():
    args = urlparse.parse_qs(sys.argv[2][1:])
    mode = args.get('mode', None)
    folder = args.get('folder', '0')

    if mode is None:
        createMainMenu()
    elif mode[0] == '1':
        if folder[0] == '0':
            createStationsMenu(args['sub'][0])
        elif folder[0] == '1':
            createSubStationsMenu(args['sub'][0], args['sub2'][0])

def build_url(base, query):
	return base+'?'+urllib.urlencode(query)

def createMainMenu():
    menu = 'main'
    items = loadJson(menu)
    log("(Main) createMainMenu items:%s" %items, LOGLEVEL.INFO)

    for item in items:
        log("(Main) createMainMenu item:%s" %item, LOGLEVEL.INFO)
        li = xbmcgui.ListItem(item['title'])
        url = build_url(base, {'mode': 1, 'sub': item['title']})
        xbmcplugin.addDirectoryItem(handle=handle, url=url, listitem=li, isFolder=True)

    xbmcplugin.endOfDirectory(handle)

def createStationsMenu(sub):
    log("(Main) createStationsMenu sub:%s" %sub, LOGLEVEL.INFO)
    items = loadJson(sub)
    log("(Main) createStationsMenu items:%s" %items, LOGLEVEL.INFO)

    for item in items:
        if 'folder' in item:
            folder = item['folder']
            li = xbmcgui.ListItem(item['title'], iconImage=item['image'])
            url = build_url(base, {'mode': 1, 'sub': sub, 'sub2': item['title'], 'folder': item['folder']})
            xbmcplugin.addDirectoryItem(handle=handle, url=url, listitem=li, isFolder=True)
        else:
            log("(Main) createStationsMenu item:%s" %item, LOGLEVEL.INFO)
            li = xbmcgui.ListItem(item['title'], iconImage=item['image'])
            url = item['stream']
            xbmcplugin.addDirectoryItem(handle=handle, url=url, listitem=li)

    xbmcplugin.endOfDirectory(handle)

def createSubStationsMenu(sub, sub2):
    log("(Main) createSubStationsMenu sub:%s" %sub, LOGLEVEL.INFO)
    items = loadJson2(sub, sub2)
    log("(Main) createSubStationsMenu items:%s" %items, LOGLEVEL.INFO)

    for item in items:
        log("(Main) createSubStationsMenu item:%s" %item, LOGLEVEL.INFO)
        li = xbmcgui.ListItem(item['title'], iconImage=item['image'])
        url = item['stream']
        xbmcplugin.addDirectoryItem(handle=handle, url=url, listitem=li)

    xbmcplugin.endOfDirectory(handle)

if __name__ == '__main__':
    handle = int(sys.argv[1])
    # when addon is launched check if new version of radio list is available
    checkVer()
    main()
