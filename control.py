from pygame import draw,font,Rect,image
import math

class control(object):
    def __init__(self,posx,posy,width,height):
        self._pos = (posx,posy)
        self._size = (width,height)
        self._background = None


    def setBackground(self,backpath):
        self._background = image.load(backpath)
        #self._background.set_colorkey((0,0,255), pygame.RLEACCEL)

    def draw(self):
        pass



class listview(control):
    def __init__(self,x,y,width,height,columns):
        control.__init__(self,x,y,width,height)
        self._curindex = None
        self._listitems = []
        self._columnstarts = columns
        self._yOffset = 0
        self._fonten = font.Font(None,20)
        self._topDisplayItem = 0
        self._itemsPerPage = int(math.floor((height-2*self._yOffset) / (self._fonten.get_height() + 7)))
        self._displayselection = True

    def getSelectedIndex(self):
        return self._topDisplayItem + self._curindex
        
    def getSelectedItem(self):
        return self._listitems[self.getSelectedIndex()]

    def setYOffset(self,offset):
        self._yOffset = offset

    def setColumns(self,z):
        self._columnstarts = z
        
    def draw(self,screen):
        #draw listcontrol as white? box
        #draw listitems as text, icons available
        #current item as marked?
        if self._background != None:
            screen.blit(self._background,self._pos)
        else:
            draw.rect(screen, (205,202,255), Rect(self._pos,self._size))
            
        if self._curindex != None and self._displayselection:
            draw.rect(screen, (88,100,241), Rect( (self._pos[0] + 10), (self._pos[1]+6 + self._yOffset + (self._curindex * 18)),self._size[0]-20,20))

        for y,item in enumerate(self._listitems[self._topDisplayItem: (self._topDisplayItem + self._itemsPerPage)]):
            if type(item) is str:
                item = [item]
                
            for i,x in enumerate(self._columnstarts):
                if i + 1 > len(self._columnstarts) - 1:
                    stop = self._size[0] - 10
                else:
                    stop = self._columnstarts[i+1] - x - 10

                tmp = item[i]
                while self._fonten.size(tmp)[0] > stop:
                    tmp= tmp[0:-1]
                    
                tmpfont = self._fonten.render(tmp,True,(0,0,0))
                screen.blit(tmpfont, (self._pos[0]+x, self._pos[1]+10 + self._yOffset + (y * 18)))
                
    def scrollDown(self):
        if self._curindex == None:
            self._curindex = -1
            
        self._curindex += 1
        if self.getSelectedIndex() > len(self._listitems)-1:
            self._curindex = 0
            self._topDisplayItem = 0
        elif self._curindex > self._itemsPerPage-1 or self._curindex > len(self._listitems)-1:
            self._topDisplayItem += 1
            self._curindex -= 1

    def scrollUp(self):
        if self._curindex == None:
            self._curindex = len(self._listitems)
         
        self._curindex -= 1
        if self.getSelectedIndex() < 0:
            self._curindex = self._itemsPerPage-1
            self._topDisplayItem = len(self._listitems) - self._itemsPerPage
        elif self._curindex < 0:
            self._topDisplayItem -= 1
            self._curindex += 1

    def setItems(self,listitems):
        self._listitems = listitems
        self._curindex = 0
        self._topDisplayItem = 0

    def appendItem(self,item):
        tmp = self._listitems
        tmp[0:] = item
        self.setItems(tmp)

    def setSelected(self,id):
        self._curindex = id

class imagecontrol(control):
    def __init__(self,x,y):
        control.__init__(self,x,y,0,0)
        self._image = None

    def setImage(self,param):
        if type(param) is str:
            self._image = image.load(param)
        else:
            self._image = param

    def draw(self,screen):
        if self._image != None:
            screen.blit(self._image,self._pos)

class label(control):
    def __init__(self,x,y,color=(0,0,0),size=20):
        control.__init__(self,x,y,0,0)
        self._text = ""
        self._fontsize = size
        self._color = color

    def setText(self,text):
        self._text = text

    def draw(self,screen):
        fonten = font.Font(None,self._fontsize)
        screen.blit(fonten.render(self._text,True,self._color), self._pos)

ErrType = 1
InfoType = 2

class overlay(control):
    def __init__(self,owner,type,text):
        control.__init__(self,0,330,600,150)
        self._background = image.load("images/overlay.png")
        self._lifecounter = 0
        self._owner = owner
        self._text = text
        owner.addControl(self)

        if type == ErrType:
            self._icon = image.load("images/erricon.png")
        else:
            self._icon = image.load("images/infoicon.png")

    def draw(self,screen):
        screen.blit(self._background,self._pos)
        screen.blit(self._icon, (13,395))

        fonten = font.Font(None,25)
        screen.blit(fonten.render(self._text,True,(0,0,0)), (100,435))

        self._lifecounter += 1
        if self._lifecounter == 60:
            self._owner._controls.remove(self)
        
