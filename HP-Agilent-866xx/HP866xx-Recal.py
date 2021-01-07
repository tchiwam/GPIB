from gpibeth import gpibeth
from time import sleep

GPIBHOST = "192.168.0.118"
GPIBPORT = 1234
GPIBADDR = 25

HP866xx = gpibeth(GPIBHOST,GPIBPORT,GPIBADDR)
#HP866xx.setverbose(True)
HP866xx.send('*RST')
sleep(2)
print(HP866xx.getvalue("*IDN?"))
print(HP866xx.getvalue("*OPT?"))

HP866xx.send(f"DIAG:LATCH:MOD 12")
HP866xx.send(f"DIAG:LATCH:NUMBER 100")
HP866xx.send(f"DIAG:LATCH:DATA 0")
HP866xx.send(f"DIAG:LATCH:NUMBER 101")
Mwext_elements = int(HP866xx.getvalue(f"DIAG:LATCH:DATA?"))

Vern_elements = 25
Alc_elements = 38
Total_elements = Alc_elements+Vern_elements+Mwext_elements

Data = [0   for i in range(Total_elements)]
print("Vern_elements  :", Vern_elements)
print("Alc_elements   :", Alc_elements)
print("Mwext_elements :", Mwext_elements)

print("MOD 5 Freq")
HP866xx.send(f"DIAG:LATCH:MOD 5")
for Freq in range(Alc_elements):
    HP866xx.send(f"DIAG:LATCH:NUMBER 100")
    HP866xx.send(f"DIAG:LATCH:DATA 0")
    HP866xx.send(f"DIAG:LATCH:NUMBER 104")
    HP866xx.send(f"DIAG:LATCH:DATA {Freq:d}")
    HP866xx.send(f"DIAG:LATCH:NUMBER 105")
    Data[Freq] = int(HP866xx.getvalue(f"DIAG:LATCH:DATA?"))
    

print("MOD 12 Vern")
HP866xx.send(f"DIAG:LATCH:MOD 12")
for Vern in range(Vern_elements):
    HP866xx.send(f"DIAG:LATCH:NUMBER 100")
    HP866xx.send(f"DIAG:LATCH:DATA 1")
    HP866xx.send(f"DIAG:LATCH:NUMBER 104")
    HP866xx.send(f"DIAG:LATCH:DATA {Vern:d}")
    HP866xx.send(f"DIAG:LATCH:NUMBER 105")
    Data[Vern+Alc_elements] = int(HP866xx.getvalue(f"DIAG:LATCH:DATA?"))

print("MOD 12 Freq")
HP866xx.send(f"DIAG:LATCH:MOD 12")
for Freq in range(Mwext_elements):
    HP866xx.send(f"DIAG:LATCH:NUMBER 100")
    HP866xx.send(f"DIAG:LATCH:DATA 0")
    HP866xx.send(f"DIAG:LATCH:NUMBER 104")
    HP866xx.send(f"DIAG:LATCH:DATA {Freq:d}")
    HP866xx.send(f"DIAG:LATCH:NUMBER 105")
    Data[Freq+Alc_elements+Vern_elements] = int(HP866xx.getvalue(f"DIAG:LATCH:DATA?"))

print("Performing ALC and MWET Calibration on UUT...")
HP866xx.send(f"DIAG:CAL:OS:START")
for Cal_step in range(Total_elements):
    Cal_freq = float(HP866xx.getvalue("FREQ:CW?"))
    if Cal_freq == 0 :
        break
    if Cal_freq < 3.0e+9:
        Amplitude = 8.0
    if Cal_freq == 3.0e+9:
        AmplitudeValue = float(HP866xx.getvalue("AMPL:LEV?"))
        Amplitude = AmplitudeValue
    if Cal_freq > 3.0e+9:
        Amplitude = 10.0
    value = Amplitude-Data[Cal_step]/110
    print("FREQ =", Cal_freq, "Amplitude =", Amplitude, "Data =", value )
    HP866xx.send(f"DIAG:CAL:OS {value:f}")

HP866xx.send("DIAG:CAL:OS:STOP 0")
HP866xx.send("DIAG:CAL:AM:ALC:SCAL")
HP866xx.send("DIAG:CAL:AM:MWX:SCAL")
print("Performing Instrument Self Cal. Please wait.")
HP866xx.settimeout(3600)
print(HP866xx.getvalue("*CAL?"))
print("ALC and MWext Calibration COMPLETE")
HP866xx.send("*RST")

HP866xx.close()


