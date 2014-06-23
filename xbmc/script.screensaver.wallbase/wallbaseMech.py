import mechanize
import sys
from advLogger import log
from constants import _loginUrl, _user, _pass
from constants import _wallpageSearchString, _wallSearchString
from constants import _testingMainUrl

class WallbaseWeb:
    def __init__(self):
        self.connect()
    
    def login(self):
        response = self.browser.open(_loginUrl)  # open login page
        self.browser.form = list(self.browser.forms())[0]  # use when form is unnamed
        self.browser['username'] = _user  # equivalent and more normal
        self.browser['password'] = _pass  # equivalent and more normal
        response = self.browser.submit()  # login

    def connect(self):
        self.browser = mechanize.Browser()
        self.browser.set_handle_robots(False)   # ignore robots
        self.browser.set_handle_refresh(False)  # can sometimes hang without this
        self.browser.addheaders = [('User-agent', 'Firefox')]
    
    def disconnect(self):
        pass
    
    def loadImageListPuritySFW(self):
        response = self.browser.open(_testingMainUrl)
        htmlPage = response.read()
        
#        count = 0
        image = []
        
        for line in htmlPage.split('\n'):
            if _wallpageSearchString in line:
                wallPage = line.split('"')[1]

                response = self.browser.open(wallPage)
                imagePage = response.read()
                
                for imageUrl in imagePage.split('\n'):
                    if _wallSearchString in imageUrl:
                        log(imageUrl.split('"')[1])
                        image.append(imageUrl.split('"')[1])
#                        count = count + 1
        
#            if count == 2:
#                break
            
        return image

    def loadImageList(self, url):
        response = self.browser.open(url)
        htmlPage = response.read()
        
        image = []
        
        # get list of pages with the images
        for line in htmlPage.split('\n'):
            if _wallpageSearchString in line:
                wallPage = line.split('"')[1]

                response = self.browser.open(wallPage)
                imagePage = response.read()
                
                # get actual image url from the page
                for imageUrl in imagePage.split('\n'):
                    if _wallSearchString in imageUrl:
                        log(imageUrl.split('"')[1])
                        image.append(imageUrl.split('"')[1])
                        
        return image
    
    def setOptions(self):
        pass