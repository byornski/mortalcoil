import board
import requests


def getBoard(username,password,levelnumber=None):
    '''Get the next (or specified) level from the mortal coil game'''
    import re
    
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
    print r.url



    #Grab the level number from the response
    try:
        levelnumber = int(re.findall('</table>Level: (\d+)<br>',r.text)[0])
    except:
        "Error getting level number from server"


    
    #Lets try and parse it for board info
    try:
        boardinfo = re.findall('name="FlashVars".*x=(\d+)&y=(\d+)&board=(.+)".*/>',r.text)[0]
    except:
        #Server returns reasonably useful responses
        raise Exception(r.text)

    return board.board(levelnumber,*boardinfo)

