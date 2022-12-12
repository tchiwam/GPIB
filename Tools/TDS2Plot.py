import matplotlib.pyplot as plt
from matplotlib import colors

from gpibeth import gpibeth
from time import sleep

GPIBHOST = "172.20.0.51"
GPIBPORT = 1234
GPIBADDR = 1

gpib = gpibeth(GPIBHOST,GPIBPORT,GPIBADDR)
#gpib.setverbose(True)

print("Prologix Ethernet version: ", gpib.getvalue("++ver"))

gpib.send("*RST")
print(gpib.getvalue("*IDN?"))
print(gpib.getvalue("*OPT?"))
# FIXME: Set time of instrument then check it
print(gpib.getvalue("DATE?"))
print(gpib.getvalue("TIME?"))

# Set trigger
gpib.send("CLEARMENU")
gpib.send("TRIGGER:MAIN:EDGE:SOURCE CH1")
gpib.send("TRIGGER:MAIN:LEVEL 0.01")
gpib.send("TRIGGER:MAIN:HOLDOFF:TIME 0.0")
gpib.send("HORIZONTAL:TRIGGER:POSITION 10")
gpib.send("DISPLAY:TRIGT ON")


# Set buffer length and display window
gpib.send("HORIZONTAL:FITTOSCREEN ON")
gpib.send("HORIZONTAL:RECORDLENGTH 120000")
gpib.send("HORIZONTAL:MAIN:SCALE 100.0E-9")
gpib.send("HORIZONTAL:DELAY:SCALE 100.0E-9")
gpib.send("HORIZONTAL:DELAY:SECDIV 100.0E-9")
gpib.send("DISPLAY:CLOCK ON")
gpib.send("DATA:ENC ASCII")
gpib.send("DATA:SOURCE CH1")
gpib.send("DATA:START 1")
gpib.send("DATA:STOP 120000")
gpib.send("CH1:POS 0.0")
gpib.send("CH1:VOLTS 15E-03")
gpib.send("CH1:DESK 0.0")
gpib.send("CH1:COUP DC")
gpib.send("CH1:BANDWIDTH FULL")

gpib.send("ACQUIRE:MODE SAMPLE")
gpib.send("ACQUIRE:STOPAFTER SEQUENCE")
gpib.send("ACQUIRE:STATE RUN")

waiting = gpib.getvalue("ACQUIRE:STATE?")
timeout = 0
while waiting != '0' and timeout <10:
    print("waiting for data",timeout)
    sleep(1)
    timeout +=1
# Get the curve
gpib.settimeout(10)
data = list(map(int,gpib.getvalue("CURV?",eol=0x0a).split(",")))
print(data)
#gpib.send("*RST")

gpib.close()

plt.plot(data)
plt.title("Channel 1")
plt.suptitle("samples")
plt.xlabel("Sample #")
plt.ylabel("Value")
plt.show()

