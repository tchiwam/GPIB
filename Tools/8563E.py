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
{'cf': 3350000000, 'bw': 3000, 'span': 30000000,'rl':20,'N':10},
{'cf': 3350000000, 'bw': 1000, 'span': 10000000,'rl':20,'N':10},
{'cf': 3350000000, 'bw': 100, 'span': 1000000,'rl':10,'N':10},
{'cf': 3350000000, 'bw': 10, 'span': 100000,'rl':0,'N':10},
{'cf': 3350000000, 'bw': 1, 'span': 1000,'rl':20,'N':10},
{'cf': 3350000000, 'bw': 1, 'span': 100,'rl':20,'N':10},
{'cf': 3350000000, 'bw': 10, 'span': 1000000,'rl':-40,'N':10},
{'cf': 3350000000, 'bw': 1,  'span': 100000,'rl':-50,'N':10},
]


for meas in measurements:
    gpib.send("SNGLS;")
    gpib.send("CF %d;" % meas['cf'])
    gpib.send("SP %d;" % meas['span'])
    gpib.send("ST AUTO;")
    gpib.send("VAVG 1;")
    gpib.send("RB %d;" % meas['bw'])
    gpib.send("RL %d;" % meas['rl'])
    gpib.send("AT AUTO;")

    amplUnits  = gpib.getvalue("AUNITS?;")
    amplRefLvl = float(gpib.getvalue("RL?;"))
    amplAtt    = float(gpib.getvalue("AT?;"))
    sweepMeas  = gpib.getvalue("MEAS?;")
    sweepTime  = float(gpib.getvalue("ST?;"))
    bwRes      = float(gpib.getvalue("RB?;"))
    freqCenter = float(gpib.getvalue("CF?;"))
    freqStart  = float(gpib.getvalue("FA?;"))
    freqStop   = float(gpib.getvalue("FB?;"))
    freqSpan   = float(gpib.getvalue("SP?;"))
    freqRef    = gpib.getvalue("FREF?;")

    print("Date UTC",datetime.datetime.utcnow())
    print("Amplitude Units: ", amplUnits)
    print("Amplitude Reference Level: ", amplRefLvl)
    print("Amplitude Attenuation: ", amplAtt)
    print("Sweep type:", sweepMeas)
    print("Sweep time:", sweepTime)
    print("Bandwidth Resolution :", bwRes)
    print("Center Frequency", freqCenter)
    print("Freq Start", freqStart)
    print("Freq Stop", freqStop)
    print("Freq Span", freqSpan)
    print("Freq Reference", freqRef)

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
        plt.plot(data)
    plt.title("Channel 1")
    plt.suptitle("samples")
    plt.xlabel("Freq ")
    plt.ylabel("dBm")
    plt.show()

gpib.close()
