from wlanform import *
from wlanbackend import *
from folderform import *
from musicform import *
from control import overlay,InfoType
import pygame
from pygame import display,font,event
from generic import TrackDone
from ftp import ftpBackend
from settings import *


def main():
    display.init()
    font.init()
    screen = display.set_mode((640,480))
    run = True
    background = pygame.image.load("images/background.png")
    clock = pygame.time.Clock()
    
    wbackend = wlanbackend()
    fbackend = ftpBackend()
    frmwlan = wlanform(wbackend)
    frmmusic = musicform()
    frmfolders = folderform(frmmusic)

    curConnectedWlan = None
    
    frms = [frmmusic,frmfolders,frmwlan]    
    activefrm = 0

    pygame.key.set_repeat(300,100)

    while run:
        clock.tick(20)
        if curConnectedWlan != wbackend.getConnected():
            curConnectedWlan = wbackend.getConnected()
            overlay(frms[activefrm],InfoType,"Connected to " + str(curConnectedWlan))
            print "Connected to " + str(curConnectedWlan)

        if curConnectedWlan == homeWlan:
            #fbackend.startSync()
            pass

        if fbackend.statusAvailable():
            overlay(frms[activefrm],InfoType,fbackend.getStatus())
            
        #screen.fill((27,103,245))
        screen.blit(background,(0,0))
        frms[activefrm].doFormUpdate()
        frms[activefrm].drawControls(screen)
        display.flip()
        for e in event.get():
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_KP_DIVIDE:
                    activefrm -= 1
                    if activefrm < 0:
                        activefrm = len(frms)-1
                elif e.key == pygame.K_KP_MULTIPLY:
                    activefrm += 1
                    if activefrm > len(frms)-1:
                        activefrm = 0
                elif e.key == pygame.K_KP_MINUS:
                    frmmusic.incVolume()
                elif e.key == pygame.K_KP_PLUS:
                    frmmusic.decVolume()
                else:
                    frms[activefrm].handleKeys(e.key)
                
            elif e.type == pygame.QUIT:
                run = False
            elif e.type == pygame.constants.USEREVENT:
                frmmusic.trackFinished()

    fbackend.killSyncBackend()            

if __name__ == "__main__":
    main()