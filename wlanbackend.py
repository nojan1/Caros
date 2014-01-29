from generic import runShellCmd,cleanLine
import settings
from string import atof

class wlanbackend(object):
    def __init__(self):
        self._scancommand = settings.wlanScanCommand
        self._statcommand = settings.wlanStatCommand
        self._wlanlist = [[]]
        self._intervalcounter = 200

        #temp        
        #self._intervalcounter = 0
        #self._wlanlist = [["Sitecom", "90%","Yes"],["Dlink", "50%","No"],["Hej","20%","No"]]

    def getWlans(self):
        return self._wlanlist

    def getConnectedIndex(self):
        essid = self.getConnected()
        for i,x in enumerate(self._wlanlist):
            if len(x) > 0 and x[0] == essid:
                return i
        return None

    def getConnected(self):
        #line = cleanLine(runShellCmd(self._statcommand).split("\n")[0])
        #start = line.find("ESSID:")
        #essid = line[start+6:]
        #return essid
        return "Hedlunds"
        
    def process(self):
        if self._intervalcounter != 200:
            #self._intervalcounter += 1
            return
        self._intervalcounter = 0
        self._wlanlist = []
        essid = strength = enc = ""
        for line in map(lambda x: cleanLine(x),runShellCmd(self._scancommand).split("\n")):
            if line[0:7] == "ESSID:\"":
                essid = line[7:-1]

            if line[0:15] == "Encryption key:":
                enc = line[15:]

            if line[0:8] == "Quality=":
                level,max = line[8:13].split("/")
                pro = int((atof(level)/atof(max))*100)
                strength = str(pro)+ "%"
            
            if essid != "" and strength != "" and enc != "":
                self._wlanlist.append( [essid,strength,enc] )
                essid = strength = enc = ""
        
        
        