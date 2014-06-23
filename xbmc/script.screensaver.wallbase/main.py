import xbmcgui
import sys
from xbmcgui import WindowDialog
from advLogger import log
from wallbaseMech import WallbaseWeb
from constants import _changeInterval, _waitChunkSize, _imageReloadLimit
from constants import _onlineTesting, _defaultImage1, _defaultImage2
from constants import _baseUrl, _searchRandom, _searchTop, _searchPurity, _loadRandom

from constants import _liveEnabled

class ExitMonitor(xbmc.Monitor):
    def __init__(self, exit_callback):
        self.exit_callback = exit_callback

    def onScreensaverDeactivated(self):
        log('Exit Recieved: Sending exit_callback')
        self.exit_callback()

class PopupWindow(WindowDialog):
    def __init__(self):
        log("__init__")
        self.closeCalled = False
        self.control = xbmcgui.ControlImage(x=0, y=0, width=1280, height=720, aspectRatio=2, filename=_defaultImage1)
        self.addControl(self.control)
        #self.addControl(xbmcgui.ControlLabel(x=0, y=0, width=1280, height=720, label='Spardz\nThis is how we do it!'))
        self.show()
        
        self.exit_callback = self.stop
        self.exit_monitor = ExitMonitor(self.stop)
        
        self.setupBrowser()
    
    def setupBrowser(self):
        self.browser = WallbaseWeb()
        #self.browser.login()
        self.image = self.browser.loadImageListPuritySFW()
        
        log(', '.join(self.image))
    
    def changeImage(self, imageUrl, index):
        log("Changing Image: " + str(index) + " " + str(self.closeCalled))
        #self.removeControl(self.control)
        self.control.setImage(imageUrl)
        #self.addControl(self.control)
    
    def loop(self):
        changeTime = _changeInterval
        count = 0
        while self.closeCalled == False:
            if count == 0:
                if _onlineTesting:
                    temp = self.image.pop(0)
                    self.changeImage(temp, count)
                    self.image.append(temp)
                else:
                    self.changeImage(_defaultImage1, count)
            elif count == 1:
                if _onlineTesting:
                    temp = self.image.pop(0)
                    self.changeImage(temp, count)
                    self.image.append(temp)
                else:
                    self.changeImage(_defaultImage2, count)
                
            self.wait(changeTime)
            if count == 1:
                count = 0
            else:
                count = count + 1
    
    def onAction(self, action):
        action_id = action.getId()
        if action_id in ACTION_IDS_EXIT:
            self.exit_callback()
        
    def wait(self, totalTime):
        i = 0
        while i < totalTime and self.closeCalled == False:
            xbmc.sleep(_waitChunkSize)
            i = i + _waitChunkSize
    
    def stop(self):
        log('Stop Called')
        self.closeCalled = True
        self.exit_monitor = None

        
class ScreenSaver(WindowDialog):
    def __init__(self):
        log('Start')
        
        self.closeCalled = False
        
        # load default image (For Pony)
        self.defaultControl = xbmcgui.ControlImage(x = 0, y = 0, width = 1280, height = 720, aspectRatio = 2, filename = _defaultImage1)
        self.addControl(self.defaultControl)
        self.show() # show default picture at startup
        
        self.exit_callback = self.stop # function to call when exit is triggered
        self.exit_monitor = ExitMonitor(self.stop) # add monitor to key stokes
        
        # list of next images and controls to show images
        self.imageList = []
        self.controlList = []
        self.imageIndex = 0
        
        self.initialSetup()

        log('End')
        
    def initialSetup(self):
        log('Start')
        
        self.browser = WallbaseWeb() # create browser object
        self.browser.login() # login to site
        
        # get first images
        self.control1 = xbmcgui.ControlImage(x = 0, y = 0, width = 1280, height = 720, aspectRatio = 2, filename = self.getNextImage())
        self.control2 = xbmcgui.ControlImage(x = 0, y = 0, width = 1280, height = 720, aspectRatio = 2, filename = self.getNextImage())
        
        TILT_ANIMATION = (
            'effect=rotatex start=0 end=55 center=auto time=0 '
            'condition=true'
        )
        MOVE_ANIMATION = (
            'effect=slide start=0,1280 end=0,-2560 time=%d '
            'tween=linear condition=true'
        )
        animations = [('conditional', TILT_ANIMATION), ('conditional', MOVE_ANIMATION % _changeInterval)]
        
        self.control1.setAnimations(animations)
        self.control2.setAnimations(animations)
        
        # remove default image and start screensaver
        self.addControl(self.control1)
        self.removeControl(self.defaultControl)
        
        # add controls to list for future use
        self.controlList.append(self.control1)
        self.controlList.append(self.control2)
        
        self.wait()
        
        log('End')
        
    def changeImage(self):
        # change image, add cache for new images
        log('Start')
        
        # show new image and remove older image
        self.addControl(self.controlList[1])
        self.removeControl(self.controlList[0])
        
        # get the control of the old image and update it's image
        chControl = self.controlList.pop(0)
        chControl.setImage(self.getNextImage())
        
        # add the control back to the list
        self.controlList.append(chControl)
        
        log('End')
    
    def getNextImage(self):
        log('Start')
        
        log('imageList Length: %d' % len(self.imageList))
        
        if len(self.imageList) < _imageReloadLimit:
            # get new images and increment index
            newList = self.browser.loadImageList(self.makeUrl())
            self.imageIndex = self.imageIndex + len(newList)
            self.imageList = self.imageList + newList
        
        log('End')
        
        return ''.join(self.imageList.pop(0))
        
    def makeUrl(self):
        log('Start')
        
        if _loadRandom:
            url = _baseUrl + (_searchRandom % self.imageIndex) + _searchPurity
        else:
            url = _baseUrl + (_searchTop % self.imageIndex) + _searchPurity
            
        log(url)
        
        log('End')
        
        return url
    
    def loop(self):
        log('Start')
        
        while self.closeCalled == False:
            log('Starting loop')
            self.changeImage()
            self.wait()
            
        log('End')
        
    def onAction(self, action):
        log('Start')
        
        action_id = action.getId()
        if action_id in ACTION_IDS_EXIT:
            self.exit_callback()
            
        log('End')
        
    def wait(self, totalTime = -1):
        log('Start')
        
        if totalTime == -1:
            totalTime = _changeInterval
        
        # wait in small chunks to allow exit
        i = 0
        while i < totalTime and self.closeCalled == False:
            xbmc.sleep(_waitChunkSize)
            i = i + _waitChunkSize
    
        log('End')
        
    def stop(self):
        log('Start')
        
        self.closeCalled = True
        self.exit_monitor = None
        
        log('End')
        
if __name__ == '__main__':
    log('Start')
    
    if _liveEnabled:
        window = ScreenSaver()
    else:
        window = PopupWindow()

    try:
        window.loop()
        log("Ending script " + str(window.closeCalled))
    except:
        window.close()
        del window

    window.close()
    del window
    log('Cleanup Finished')
    
    log('End')