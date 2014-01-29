from form import *
from control import *
import pygame

class wlanform(form):
    def __init__(self,backend):
        form.__init__(self)
        self._wlanlist = listview(20,40,600,400,[20,500,550])
        self._wlanlist.setBackground("images/wlanlist.png")
        self._wlanlist.setYOffset(20)
        self._backend = backend
        self.addControl(self._wlanlist)
        self._keydict = {pygame.K_KP8: self._wlanlist.scrollUp, pygame.K_KP2: self._wlanlist.scrollDown}

    def doFormUpdate(self):
        self._backend.process()
        self._wlanlist.setItems(self._backend.getWlans())
        

