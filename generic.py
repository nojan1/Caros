import subprocess

TrackDone = 4332535

def runShellCmd(cmd):
    p = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
    return p.stdout.read()

def cleanLine(line):
    return line.strip()

def convertTime(secs):
    mins = int(secs/60)
    secs2 = secs - (mins*60)
    return "%02d:%02d" % (mins, secs2)