class form(object):
    def __init__(self):
        self._controls = []
        self._keydict = {}

    def addControl(self,ctrl):
        self._controls.append(ctrl)

    def drawControls(self,screen):
        for c in self._controls: c.draw(screen)

    def doFormUpdate(self):
        pass

    def handleKeys(self,key):
        if self._keydict.has_key(key) and callable(self._keydict[key]):
            self._keydict[key]()