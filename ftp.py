from ftplib import FTP
from settings import *
from threading import Thread
import os

class ftpHandler(object):
    def __init__(self,host,port,user,passw):
        try:
            self._ftp = FTP()
            self._ftp.connect(host,port)
            self._ftp.login(user,passw)
        except:
            pass

    def setPassive(self,bool):
        if self._ftp != None:
            self._ftp.set_pasv(bool)

    def downloadFile(self,src,dst):
        if self._ftp != None:
            print "Downloading",src,"to",dst
            self._ftp.retrbinary('RETR '+src, open(dst, 'wb').write)

    def storeLines(self,val):
        return self.files.append(val)

    def getFilesRecursive(self,path):
        l= []
        for r in self._ftp.nlst(path):
            if not "." in r:
                for tmp in self.getFilesRecursive(r):
                    l.append(tmp)
            else:
                if not "Thumbs.db" in r:
                    l.append(r)
                
        return l
            

class ftpBackend(Thread):
    def __init__(self):
        Thread.__init__(self)
        self._counter = 7100
        self.workDir = musicBasePath+"/Temp"
        self.templateDir = ""
        self._status = None

    def startSync(self):
        if self._counter == 7200:
            if self.isAlive() == False:
                self._counter = 0
                self._status = "Auto Synchronization started..."
                self.start()
        else:
            self._counter += 1

    def statusAvailable(self):
        return self._status != None

    def getStatus(self):
         tmp = self._status
         self._status = None
         return tmp

    def buildDirPath(self,dirNames, level):
        dir = dirNames[0]
        for i in range(level+1)[1:]:
            dir = os.path.join(dir, dirNames[i])
    
        return os.path.join(self.workDir,dir)    
    
    def attemptDirRemove(self,path):
        dirnames = path.split("/")
        curLevel = len(dirnames) - 2
        curDir = self.buildDirPath(dirnames, curLevel)
        while len(self.getRelFilelist(curDir)) == 0:
            print "Removing",curDir
            os.rmdir(curDir)
            curLevel -= 1
            if curLevel < 2: break
            curDir = self.buildDirPath(dirnames, curLevel)

    def createDirs(self,path):
        dirnames = path.split("/")
        for i in range(len(dirnames) - 1):
            curDir = self.buildDirPath(dirnames, i)
            if os.path.isdir(curDir) == False:
                print "Creating", curDir
                os.mkdir(curDir)
            else:
                print "Path",curDir,"exists"
            
    def getRelFilelist(self,path):
        l = []    
        for dirpath,dirnames,files in os.walk(path):
            for file in files:
                tmp = os.path.join(dirpath, file).replace("\\","/")
                l.append(tmp[len(path)+1:])

        return l

    def killSyncBackend(self):
        try:
            self._ftp.abort()
            self._ftp.close()
        except:
            pass
        
        while self.isAlive():
            self.join()
    
    def run(self):
        ftp = ftpHandler(ftpHost,ftpPort,ftpUser,ftpPass)
        ftp.setPassive(ftpUsePassive)

    
        templateFiles = ftp.getFilesRecursive(self.templateDir)
        workFiles = self.getRelFilelist(self.workDir)

        if len(templateFiles) != 0:    
            for name in templateFiles:
                if name in workFiles:
                    workFiles.remove(name)  
                    templateFiles.remove(name)
    
            print len(templateFiles), "file(s) to copy"
            print len(workFiles), "file(s) to remove"

            for fileToDel in workFiles:
                try:
                    path = os.path.join(self.workDir, fileToDel)
                    print "Deleting:",path
                    os.remove(path)
                    self.attemptDirRemove(fileToDel)
                except:
                    print "Failed to delete",fileToDel
    
            for fileToCpy in templateFiles:
                try:
                    srcPath = os.path.join(self.templateDir, fileToCpy)
                    dstPath = os.path.join(self.workDir, fileToCpy)
                    self.createDirs(fileToCpy)
                    ftp.downloadFile(srcPath,dstPath)
                except:
                    print "Failed to download",srcPath

        print "Done!"
        ftp._ftp.close()
        self._status = "Synchronization  completed"
        
        
        
        