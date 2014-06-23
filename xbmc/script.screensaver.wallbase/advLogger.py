import xbmc
import xbmcaddon
import inspect
from constants import _isLoggingEnabled, _loggingTag

addon = xbmcaddon.Addon()
ADDON_NAME = addon.getAddonInfo('name')
ADDON_PATH = addon.getAddonInfo('path')

def log(text):
    if _isLoggingEnabled:
        print _loggingTag + ' INFO - ' + inspect.stack()[1][3] + ' - ' + text
    
def __init__():
    print ADDON_NAME
    
log("Initializing: " + addon.getAddonInfo('name'))