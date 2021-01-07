from gpibeth import gpibeth
from time import sleep
import matplotlib.pyplot as plt


GPIBHOST = "192.168.0.118"
GPIBPORT = 1234
GPIBADDR = 8

FreqStart = 100e6
FreqStop  = 4500e6
FreqStep  = 1e5
FreqBins  = range(int(FreqStart),int(FreqStop),int(FreqStep))
s11  = [float(0.0) for i in range(len(FreqBins)) ]
s12  = [float(0.0) for i in range(len(FreqBins)) ]

gpib = gpibeth(GPIBHOST,GPIBPORT,GPIBADDR)
#gpib.setverbose(True)

print("Prologix Ethernet version: ", gpib.getvalue("++ver"))

gpib.setaddr(25)
print(gpib.getvalue("*IDN?"))
print(gpib.getvalue("*OPT?"))
gpib.send('AMPL:STATE OFF')
gpib.send('FREQ 50MHZ')
gpib.send('AMPL 0DBM')
sleep(5)

gpib.setaddr(8)
gpib.send("SYST:LANG SCPI")
gpib.send("*RST")
print(gpib.getvalue("*IDN?"))
print(gpib.getvalue("*OPT?"))
gpib.send("CAL1:ZERO:AUTO ONCE")
gpib.send("CAL2:ZERO:AUTO ONCE")

sleep(5)
gpib.setaddr(25)
gpib.send('AMPL:STATE ON')
gpib.setaddr(8)
#gpib.send("CAL2:AUTO ONCE")

gpib.send("DISPLAY:WIND1:RES 4")
gpib.send("DISPLAY:WIND2:RES 4")

gpib.send("ABORT1")
gpib.send("ABORT2")
gpib.send("SENS1:FREQ 500KHZ")
gpib.send("SENS2:FREQ 500KHZ")
gpib.send("SENS1:AVER:COUNT 100")
gpib.send("SENS2:AVER:COUNT 100")
gpib.send("SENS1:AVER:STATE ON")
gpib.send("SENS2:AVER:STATE ON")

gpib.send("SENS1:SPE 40")
gpib.send("SENS2:SPE 40")
print("SENSE speed port 1",float(gpib.getvalue("SENS1:SPE?")))
print("SENSE speed port 2",float(gpib.getvalue("SENS2:SPE?")))
gpib.send("SENS1:CORR:GAIN2 40")
gpib.send("SENS2:CORR:GAIN2 0")
print("System LOSS port 1",float(gpib.getvalue("SENS1:CORR:GAIN2?")))
print("System LOSS port 2",float(gpib.getvalue("SENS2:CORR:GAIN2?")))

print(float(gpib.getvalue("READ1?")))
print(float(gpib.getvalue("READ2?")))

gpib.send("SENS1:AVER:COUNT 1")
gpib.send("SENS2:AVER:COUNT 1")
gpib.send("SENS1:AVER:STATE OFF")
gpib.send("SENS2:AVER:STATE OFF")
gpib.send("INIT1:CONT ON")
gpib.send("TRIG1:SOURCE IMM")
gpib.send("INIT2:CONT ON")
gpib.send("TRIG2:SOURCE IMM")

plt.title("Scalar Network Analyzer")
plt.xlabel("Frequency (Hz)")
plt.ylabel("Power (dBm) ")
plt.axis([FreqBins[0],FreqBins[-1],-50,15])
for i in range(len(FreqBins)):
    gpib.setaddr(25)
    gpib.send(f'FREQ {FreqBins[i]:.0f}')
    #Freq = gpib.getvalue("FREQ?")
    Freq = FreqBins[i] 
    gpib.setaddr(8)
    s11[i] = float(gpib.getvalue("FETC1?"))
    s12[i] = float(gpib.getvalue("FETC2?"))
    print("Frequency : ",Freq,"s11 : ",s11[i],"s12 : ",s12[i])
    plt.plot(FreqBins[i],s11[i],label="s11")
    plt.plot(FreqBins[i],s12[i],label="s12")
    plt.pause(0.05)
plt.close()
plt.title("Scalar Network Analyzer")
plt.xlabel("Frequency (Hz)")
plt.ylabel("Power (dBm) ")
plt.axis([FreqBins[0],FreqBins[-1],-50,5])
plt.plot(FreqBins,s11,zorder=1,label="s11")
plt.plot(FreqBins,s12,zorder=2,label="s12")
plt.legend()
plt.show()

gpib.send("*RST")


gpib.close()
