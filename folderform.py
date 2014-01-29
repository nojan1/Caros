from form import *
from control import *
import pygame
import os
import settings

class folderform(form):
    def __init__(self,musicform):
        form.__init__(self)
        self._folderlist = listview(20,40,250,420,[10])
        self._filelist = listview(300,40,280,260,[10])
        self._musicform = musicform

        self._folderlist.setBackground("images/folderbackground.png")
        self._filelist.setBackground("images/filebackground.png")

        self._folderlist.setYOffset(20)
        self._filelist.setYOffset(15)

        self._filelist._displayselection = False        
        
        self.addControl(self._folderlist)
        self.addControl(self._filelist)

        self._curpath = settings.musicBasePath
        self._filesInDir = []
        self._activelist = self._folderlist

        self._keydict = {pygame.K_KP8: self.scrollUp, pygame.K_KP2: self.scrollDown, pygame.K_KP4: self.selectFolderList, pygame.K_KP6: self.selectFileList, pygame.K_KP_ENTER: self.openNewDir, pygame.K_KP5: self.playCurFile, pygame.K_KP7: self.loadCurrentDir, pygame.K_KP9: self.loadMarkedDir}
        self.openDir()        

    def playCurFile(self):
        if self._activelist is self._filelist:
            file = os.path.join(self._curpath, self._filelist.getSelectedItem())
            self._musicform.loadPlaylist([file])
            self._musicform.trackFinished()
        else:
            self.openNewDir()

    def loadCurrentDir(self):
        self.playlistFromDir(self._curpath)

    def loadMarkedDir(self):
        if self._activelist is self._folderlist:
            self.playlistFromDir(os.path.abspath(os.path.join(self._curpath,self._folderlist.getSelectedItem())))           

    def playlistFromDir(self,path):
        list = os.listdir(path)
        tmp = []
        for l in list:
            if l.split(".")[-1] in settings.allowedFileTypes:
                tmp.append(os.path.join(path,l))

        self._musicform.loadPlaylist(tmp)
        self._musicform.trackFinished()                  

    def scrollUp(self):
        self._activelist.scrollUp()

    def scrollDown(self):
        self._activelist.scrollDown()        

    def selectFolderList(self):
        self._folderlist._displayselection = True
        self._filelist._displayselection = False
        self._activelist = self._folderlist

    def selectFileList(self):
        self._folderlist._displayselection = False
        self._filelist._displayselection = True
        self._activelist = self._filelist

    def openNewDir(self):
        if self._activelist is self._folderlist:
            self._curpath = os.path.abspath(os.path.join(self._curpath, self._folderlist.getSelectedItem()))
            self.openDir()

    def openDir(self):
        for crap,dirs,self._filesInDir in os.walk(self._curpath):
            for f in self._filesInDir:
                if f.split(".")[-1] not in settings.allowedFileTypes:
                    self._filesInDir.remove(f)
                    
            self._filelist.setItems(self._filesInDir)
            dirs[:0] = ["../"]
            self._folderlist.setItems(dirs)
            break
        

        
