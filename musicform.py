from form import *
from control import *
import pygame
import os.path
import os
#from ID3 import *
from pygame import mixer
from generic import TrackDone,convertTime


class musicform(form):
    def __init__(self):
        form.__init__(self)
        mixer.init()
        self._musiclist = listview(20,180,600,250,[18,450])
        self._playinfo = label(20,70, (0,0,0), 30)
        self._playtime = label(20,105, (0,0,0), 25)
        self._revimg = imagecontrol(30,20)
        self._stopimg = imagecontrol(70,20)
        self._playimg = imagecontrol(110,20)
        self._fwdimg = imagecontrol(150,20)

        self._playinfo.setText("Not playing")
        self._playtime.setText("")
        self._revimg.setImage("images/rew.png")
        self._stopimg.setImage("images/stop_active.png")
        self._playimg.setImage("images/play.png")
        self._fwdimg.setImage("images/fwd.png")
        #self._musiclist.setItems([["Fin fin lat","Bra artist"],["Fin fin lat","Bra artist"],["Fin fin lat","Bra artist"],["Fin fin lat","Bra artist"],["Fin fin lat","Bra artist"],["Fin fin lat","Bra artist"],["Fin fin lat","Bra artist"]])
        self._musiclist.setBackground("images/musiclist.png")
        self._musiclist.setYOffset(10)
        
        self.addControl(self._musiclist)
        self.addControl(self._playinfo)
        self.addControl(self._playtime)
        self.addControl(self._revimg)
        self.addControl(self._stopimg)
        self.addControl(self._playimg)
        self.addControl(self._fwdimg)
        
        self._keydict = {pygame.K_KP8: self._musiclist.scrollUp, pygame.K_KP2: self._musiclist.scrollDown,  pygame.K_KP_ENTER: self.doNewTrack, pygame.K_KP5: self.handlePausePlay, pygame.K_KP6: self.trackFinished, pygame.K_KP0: self.doStop, pygame.K_KP4: self.prevTrack, pygame.K_KP1: self.rev, pygame.K_KP3: self.fwd}

        self._playlist = []
        self._isPaused = False
        self._isPlaying = False
        self._timeOffset = 0
        self._volume = 0.5
        mixer.music.set_endevent(pygame.constants.USEREVENT)
        pygame.event.set_allowed(pygame.constants.USEREVENT)

    def doFormUpdate(self):
        if mixer.music.get_busy() and self._isPaused == False:
            #length = ID3(self._playlist[self._musiclist.getSelectedIndex()])["LENGTH"]
            length = "xx:xx"
            totlength = (mixer.music.get_pos() / 1000) + self._timeOffset
            self._playtime.setText( str(length) + " / " + convertTime(totlength) )

    def handlePausePlay(self):
        if self._isPlaying != True:
            self.doNewTrack()
            return
            
        if self._isPaused:
            mixer.music.unpause()
            self._playimg.setImage("images/play_active.png")
            self._isPaused = False
        else:
            self._playimg.setImage("images/pause_active.png")
            mixer.music.pause()
            self._isPaused = True

    def fwd(self):
        if self._isPlaying and self._isPaused == False:
            self._timeOffset += 2
            #if self._timeOffset > trackLength:
               # self.trackFinished()

            mixer.music.play(0,self._timeOffset)

    def rev(self):
        if self._isPlaying and self._isPaused == False:
            self._timeOffset -= 2
            if self._timeOffset < 0:
                self._timeOffset = 0

            mixer.music.play(0,self._timeOffset)

    def incVolume(self):
        self._volume += 0.1
        if self._volume > 1.0:
            self._volume = 1.0

        mixer.music.set_volume(self._volume)

    def decVolume(self):
        self._volume -= 0.1
        if self._volume < 0.0:
            self._volume = 0.0

        mixer.music.set_volume(self._volume)          

    def doStop(self):
        self._stopimg.setImage("images/stop_active.png")
        self._playimg.setImage("images/play.png")
        self._playinfo.setText("Not playing")
        self._playtime.setText("")
        self._isPaused = False
        mixer.music.stop()
        self._isPlaying = False
        self._timeOffset = 0

    def doNewTrack(self):
        if self._musiclist._curindex == None:
            self._musiclist._curindex = 0
            
        self.doStop()
        try:
            mixer.music.load(self._playlist[self._musiclist.getSelectedIndex()]) 
            mixer.music.play(0,0)
            mixer.music.set_volume(self._volume)
            self._playinfo.setText("Now playing: " + self._musiclist.getSelectedItem()[0])
            self._playimg.setImage("images/play_active.png")
            self._stopimg.setImage("images/stop.png")
            self._isPlaying = True
        except:
            try:
                overlay(self,ErrType,"Failed to play track")
            except:
                pass
            
            self.trackFinished()

    def prevTrack(self):
        self._musiclist.scrollUp()
        self.doNewTrack()

    def trackFinished(self):
        self.doStop()
        self._musiclist.scrollDown()
        self.doNewTrack()

    def loadPlaylist(self,list):
        tmp = []
        self._playlist = []
        for f in list:
            if os.path.exists(f):
                self._playlist.append(f)
                #id3info = ID3(f)
                #if id3info["TITLE"] != None or id3info["TITLE"] != "":
                #	trackname = id3info["TITLE"]
                #else:
                    #trackname = f.split("/")[-1]
                trackname = f[-30:]
                
                #if id3info["ARTIST"] != None or id3info["ARTIST"] != "":
                #    artistname = id3info["ARTIST"]
                #else:
                artistname = "Unknown artist"

                tmp.append( [trackname,artistname] )	

        self._musiclist.setItems(tmp)	        