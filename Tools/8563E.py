import matplotlib.pyplot as plt
from matplotlib import colors

from gpibeth import gpibeth
from time import sleep
import datetime

GPIBHOST = "172.20.0.50"
GPIBPORT = 1234
GPIBADDR = 2

gpib = gpibeth(GPIBHOST,GPIBPORT,GPIBADDR)
#gpib.setverbose(True)

print("Prologix Ethernet version: ", gpib.getvalue("++ver"))

gpib.send("IP;")
print(gpib.getvalue("ID?;"))
print(gpib.getvalue("SER?;"))
print(gpib.getvalue("REV?;"))
gpib.send("FREF EXT;")

err = gpib.getvalue("ERR?;")
print(err)

measurements = [
{'cf':  6700000000,  'bw': '30000',  'span':  6000000000,'rl':-40,  'st': '60',   'vb':'30000'  ,'N':10},
{'cf': 12500000000,  'bw': '30000',  'span': 26500000000,'rl':0,    'st': 'AUTO', 'vb':'30000'  ,'N':10},
{'cf':  9000000000,  'bw': '30000',  'span': 12000000000,'rl':0,    'st': 'AUTO',   'vb':'30000'  ,'N':10},
{'cf': 3350000000,   'bw': 1,        'span': 100,        'rl':20,   'st': 'AUTO',   'vb':'AUTO' , 'N':10},
{'cf': 3350000000,   'bw': 1,        'span': 100,        'rl':-50,   'st': 'AUTO',   'vb':'AUTO' , 'N':10},
{'cf': 3350000000,   'bw': 10,       'span': 1000000,    'rl':-50,  'st': 'AUTO',   'vb':'AUTO' , 'N':10},
{'cf': 3350000000,   'bw': 1,        'span': 100000,     'rl':-50,  'st': 'AUTO',   'vb':'30000' , 'N':10}

]

for meas in measurements:
    gpib.send("CF %d;" % meas['cf'])
    gpib.send("SP %d;" % meas['span'])
    gpib.send("ST AUTO;")
    gpib.send("VAVG OFF;")
    if type(meas['bw']) == int or type(meas['bw']) == float:
        gpib.send("RB %d;" % meas['bw'])
    else:
        gpib.send("RB %s"  % meas['bw'])
    if type(meas['st']) == int or type(meas['st']) == float:
        gpib.send("ST %d;" % meas['st'])
    else:
        gpib.send("ST %s"  % meas['st'])
    if type(meas['vb']) == int or type(meas['vb']) == float:
        gpib.send("VB %d;" % meas['vb'])
    else:
        gpib.send("VB %s"  % meas['vb'])
    gpib.send("RL %d;" % meas['rl'])
    gpib.send("AT AUTO;")
    gpib.send("SNGLS;")

    amplUnits  = gpib.getvalue("AUNITS?;")
    amplRefLvl = float(gpib.getvalue("RL?;"))
    amplAtt    = float(gpib.getvalue("AT?;"))
    sweepMeas  = gpib.getvalue("MEAS?;")
    sweepTime  = float(gpib.getvalue("ST?;"))
    bwRes      = float(gpib.getvalue("RB?;"))
    videobw    = float(gpib.getvalue("VB?;"))
    freqCenter = float(gpib.getvalue("CF?;"))
    freqStart  = float(gpib.getvalue("FA?;"))
    freqStop   = float(gpib.getvalue("FB?;"))
    freqSpan   = float(gpib.getvalue("SP?;"))
    freqRef    = gpib.getvalue("FREF?;")
    date = datetime.datetime.utcnow()
    filename = ("8563EC-Plot-%s.txt" % date)
    f = open(filename,'w')
    print("Date UTC %s" % date)
    print("Amplitude Units: ", amplUnits)
    print("Amplitude Reference Level: ", amplRefLvl)
    print("Amplitude Attenuation: ", amplAtt)
    print("Sweep type:", sweepMeas)
    print("Sweep time:", sweepTime)
    print("Bandwidth Resolution :", bwRes)
    print("Video Bandwidth :", videobw)
    print("Center Frequency", freqCenter)
    print("Freq Start", freqStart)
    print("Freq Stop", freqStop)
    print("Freq Span", freqSpan)
    print("Freq Reference", freqRef)

    f.write("Date UTC %s \n" % date)
    f.write("Amplitude Units: %s \n" % amplUnits)
    f.write("Amplitude Reference Level: %f \n" % amplRefLvl)
    f.write("Amplitude Attenuation: %f\n" % amplAtt)
    f.write("Sweep type: %s\n" % sweepMeas)
    f.write("Sweep time: %f\n" % sweepTime)
    f.write("Bandwidth Resolution : %f\n" % bwRes)
    f.write("Video Bandwidth: %f\n" % videobw)
    f.write("Center Frequency %f\n" % freqCenter)
    f.write("Freq Start %f\n" % freqStart)
    f.write("Freq Stop %f\n" % freqStop)
    f.write("Freq Span %f\n" % freqSpan)
    f.write("Freq Reference %s\n" % freqRef)
    for i in range(meas['N']):
        gpib.send("TS;")
        sleep(sweepTime)
        gpib.settimeout(int(sweepTime*2+2))
        rawdata = gpib.getvalue("TDF P;TRA?;",eoi="\n")
        #print(rawdata)
        data = list(map(float,rawdata.split(",")))
        #freqList = range(int(freqStart),int(freqStop),int((freqStop-freqStart)/601))
        print(data)
        #print(len(data))
        #print(len(freqList))
        #plt.plot(data)

        outputString = '['
        for value in data:
            outputString += "%f ," % value
        outputString = outputString[:-1]+"]\n"
        f.write(outputString)
    #plt.title("Channel 1")
    #plt.suptitle("samples")
    #plt.xlabel("Freq ")
    #plt.ylabel("dBm")
    #plt.show()
    f.write("######################  END #####################\n")
    f.close()
gpib.close()
