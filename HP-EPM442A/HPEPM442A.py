from gpibeth import gpibeth
from time import sleep

GPIBHOST = "192.168.0.118"
GPIBPORT = 1234
GPIBADDR = 8

gpib = gpibeth(GPIBHOST,GPIBPORT,GPIBADDR)
#gpib.setverbose(True)

print("Prologix Ethernet version: ", gpib.getvalue("++ver"))

gpib.send("SYST:LANG SCPI")
gpib.send("*RST")
print(gpib.getvalue("*IDN?"))
print(gpib.getvalue("*OPT?"))

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


gpib.send("INIT1:CONT ON")
gpib.send("TRIG1:SOURCE IMM")
gpib.send("INIT2:CONT ON")
gpib.send("TRIG2:SOURCE IMM")
gpib.send("ABOR1")
gpib.send("ABOR2")


gpib.send("*RST")



gpib.close()
