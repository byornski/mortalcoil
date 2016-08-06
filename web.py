import board
import requests
import re
import os.path


def getBoard(username,password,levelnumber):
    '''Get the next (or specified) level from the mortal coil game'''

    try:
        html = getHTML(username,password,levelnumber)
        return parseHTML(html)

    except IndexError:
        #Reset the cache
        if cacheExists(levelnumber):
            resetCache(levelnumber)
            html = getHTML(username,password,levelnumber)
            return parseHTML(html)
        else:
            raise Exception(html)
        
def parseHTML(html):
    '''Parse html and return a board'''
    levelnumber = int(re.findall('</table>Level: (\d+)<br>',html)[0])
    boardinfo = re.findall('name="FlashVars".*x=(\d+)&y=(\d+)&board=(.+)".*/>',html)[0]
    return board.board(levelnumber,*boardinfo)

def getHTML(username,password,levelnumber,useCache=True):
    '''Get a level from either the cache or the web'''
    if useCache:
        if cacheExists(levelnumber):
            #Return if already in the cache
            return getCache(levelnumber)
        else:
            #Otherwise download and save
            html = getWeb(username,password,levelnumber)
            putCache(levelnumber,html)
            return html
    else:
        #No cache enabled here so just get from web
        return getWeb(username,password,levelnumber)

def resetCache(levelnumber):
    '''Delete the cache for a specific level'''
    filename = levelFile(levelnumber)
    os.remove(filename)

def putCache(levelnumber,html):
    '''Add file to the cache'''
    filename = levelFile(levelnumber)
    if os.path.isfile(filename): raise Exception("Cache exists but shouldn't")
    with open(filename,"w") as fd:
        fd.write(html)

def cacheExists(levelnumber):
    filename = levelFile(levelnumber)
    return os.path.isfile(filename)

def getCache(levelnumber):
    '''Get a file from the cache'''
    filename = levelFile(levelnumber)
    if not os.path.isfile(filename): raise Exception("Cache file does not exist")
    with open(filename) as fd:
        return fd.read()

def levelFile(levelnumber):
    return "levels/level-%d.dat" % levelnumber

def getWeb(username,password,levelnumber):
    '''Get a level from the web'''
    #Base url for the game
    baseurl = "http://www.hacker.org/coil/index.php/coil/index.php"
    
    #We always need these if we want the proper account
    auth = {
        "name" : username,
        "password"  : password,
    }

    #Go to the requested level if supplied
    if levelnumber:
        auth['gotolevel'] = levelnumber
        auth['go'] = 'Go To Level'

    #Get the http response
    r = requests.get(baseurl,params=auth)
    if "invalid password" in r.text:
        raise ValueError("Invalid username or password")
    return r.text
