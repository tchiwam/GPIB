from gpibeth import gpibeth
from time import sleep

GPIBHOST = "192.168.0.118"
GPIBPORT = 1234
GPIBADDR = 25


HP866xx = gpibeth(GPIBHOST,GPIBPORT,GPIBADDR)
#HP866xx.setverbose(True)

print("Prologix Ethernet version: ", HP866xx.getvalue("++ver"))

HP866xx.send('*RST')
sleep(2)
print(HP866xx.getvalue("*IDN?"))
print(HP866xx.getvalue("*OPT?"))

print("-------------------------")
print("Comm discrimination A6/A4")
HP866xx.send('FREQ 1GHZ')
HP866xx.send('AMPL 7.5DBM')
HP866xx.send('AMPL:STATE ON')
HP866xx.send('AM:STATE OFF')
HP866xx.send('FM:STATE OFF')
HP866xx.send('FM:DEV 1kHz')
HP866xx.send('FM:SOURCE INT')

print("Frequency    : ", HP866xx.getvalue("FREQ?"))
print("Synthesis    : ", HP866xx.getvalue("FREQ:SYNT?"))
print("Synth auto   : ", HP866xx.getvalue("FREQ:SYNT:AUTO?"))
print("Amplitude    : ", HP866xx.getvalue("AMPL?"))
print("RF           : ", HP866xx.getvalue("AMPL:STATE?"))
print("AM           : ", HP866xx.getvalue("AM:STATE?"))
print("FM           : ", HP866xx.getvalue("FM:STATE?"))

HP866xx.send('DIAG:LATCH:MOD 1')
print("Module tested : ", HP866xx.getvalue("DIAG:LATCH:MOD?"))

expected = [0.5, 1.5, 3.7, 12.4, -1.8, -1.8, 0, 0, 0, 0, -0.25, 0 , 0, 7.9, 7.3, 12.5]
print('Mux     Vdc      Vac   Expected')
for i in [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]:
    HP866xx.send(f"DIAG:LATCH:MUX {i:02d}")
    mux = int(HP866xx.getvalue("DIAG:LATCH:MUX?"))
    if mux != i:
        print(f"Failed to set MUX {i:d}")

    HP866xx.send(f"DIAG:VMETER:MODE DC")
    if HP866xx.getvalue("DIAG:VMETER:MODE?") != "DC":
        print("Failed to set VMETER to DC")
    Vdc = float(HP866xx.getvalue("DIAG:VMETER?"))

    HP866xx.send(f"DIAG:VMETER:MODE AC")
    if HP866xx.getvalue("DIAG:VMETER:MODE?") != "AC":
        print("Failed to set VMETER to AC")
    Vac = float(HP866xx.getvalue("DIAG:VMETER?"))
    print(f'{mux:>3d}  {Vdc:+7.3f}  {Vac:+7.3f}  {expected[i]:+7.3f}')


print("-----------------")
print("Frac N     A9/A10")
HP866xx.send('FREQ 1GHZ')
HP866xx.send('AMPL 10DBM')
HP866xx.send('AMPL:STATE ON')
HP866xx.send('FREQ:SYNTHESIS:AUTO OFF')
HP866xx.send('FREQ:SYNTHESIS 1')
HP866xx.send('AM:STATE OFF')
HP866xx.send('FM:STATE OFF')
HP866xx.send('FM:DEV 1kHz')
HP866xx.send('FM:SOURCE INT')

print("Frequency    : ", HP866xx.getvalue("FREQ?"))
print("Synthesis    : ", HP866xx.getvalue("FREQ:SYNT?"))
print("Synth auto   : ", HP866xx.getvalue("FREQ:SYNT:AUTO?"))
print("Amplitude    : ", HP866xx.getvalue("AMPL?"))
print("RF           : ", HP866xx.getvalue("AMPL:STATE?"))
print("AM           : ", HP866xx.getvalue("AM:STATE?"))
print("FM           : ", HP866xx.getvalue("FM:STATE?"))

HP866xx.send('DIAG:LATCH:MOD 3')
print("Module tested : ", HP866xx.getvalue("DIAG:LATCH:MOD?"))

expected = [0.076,4.49,0.76,0,0,4.8,.38,1.14]
print('Mux     Vdc      Vac   Expected')
for i in [0,1,2,3,4,5,6,7]:
    HP866xx.send(f"DIAG:LATCH:MUX {i:02d}")
    mux = int(HP866xx.getvalue("DIAG:LATCH:MUX?"))
    if mux != i:
        print(f"Failed to set MUX {i:d}")

    HP866xx.send(f"DIAG:VMETER:MODE DC")
    if HP866xx.getvalue("DIAG:VMETER:MODE?") != "DC":
        print("Failed to set VMETER to DC")
    Vdc = float(HP866xx.getvalue("DIAG:VMETER?"))

    HP866xx.send(f"DIAG:VMETER:MODE AC")
    if HP866xx.getvalue("DIAG:VMETER:MODE?") != "AC":
        print("Failed to set VMETER to AC")
    Vac = float(HP866xx.getvalue("DIAG:VMETER?"))
    print(f'{mux:>3d}  {Vdc:+7.3f}  {Vac:+7.3f}  {expected[i]:+7.3f}')

print("----------------")
print("MOD Dist A6 Test")
HP866xx.send('FREQ 3GHZ')
HP866xx.send('AMPL 7.5DBM')
HP866xx.send('AMPL:STATE ON')
HP866xx.send('AM:STATE OFF')
HP866xx.send('FM:STATE OFF')
HP866xx.send('FM:DEV 1kHz')
HP866xx.send('FM:SOURCE INT')

print("Frequency    : ", HP866xx.getvalue("FREQ?"))
print("Synthesis    : ", HP866xx.getvalue("FREQ:SYNT?"))
print("Synth auto   : ", HP866xx.getvalue("FREQ:SYNT:AUTO?"))
print("Amplitude    : ", HP866xx.getvalue("AMPL?"))
print("RF           : ", HP866xx.getvalue("AMPL:STATE?"))
print("AM           : ", HP866xx.getvalue("AM:STATE?"))
print("FM           : ", HP866xx.getvalue("FM:STATE?"))
print("FM deviation : ", HP866xx.getvalue("FM:DEV?"))
print("FM source    : ", HP866xx.getvalue("FM:SOURCE?"))

HP866xx.send('DIAG:LATCH:MOD 4')
print("Module tested : ", HP866xx.getvalue("DIAG:LATCH:MOD?"))

expected = [0.025,0.609,0.634,0,0,1.192,0,0.989]

print('Mux     Vdc      Vac   Expected')
for i in [3,4]:
    HP866xx.send(f"DIAG:LATCH:MUX {i:02d}")
    mux = int(HP866xx.getvalue("DIAG:LATCH:MUX?"))
    if mux != i:
        print(f"Failed to set MUX {i:d}")

    HP866xx.send(f"DIAG:VMETER:MODE DC")
    if HP866xx.getvalue("DIAG:VMETER:MODE?") != "DC":
        print("Failed to set VMETER to DC")
    Vdc = float(HP866xx.getvalue("DIAG:VMETER?"))

    HP866xx.send(f"DIAG:VMETER:MODE AC")
    if HP866xx.getvalue("DIAG:VMETER:MODE?") != "AC":
        print("Failed to set VMETER to AC")
    Vac = float(HP866xx.getvalue("DIAG:VMETER?"))
    print(f'{mux:>3d}  {Vdc:+7.3f}  {Vac:+7.3f}  {expected[i]:+7.3f}')

HP866xx.send('FM:DEV 1kHz')
HP866xx.send('FM:SOURCE INT')
HP866xx.send('FM:STATE ON')
print("FM           : ", HP866xx.getvalue("FM:STATE?"))
print("FM deviation : ", HP866xx.getvalue("FM:DEV?"))
print("FM source    : ", HP866xx.getvalue("FM:SOURCE?"))
for i in [0,1,5,6,7]:
    HP866xx.send(f"DIAG:LATCH:MUX {i:02d}")
    mux = int(HP866xx.getvalue("DIAG:LATCH:MUX?"))
    if mux != i:
        print(f"Failed to set MUX {i:d}")

    HP866xx.send(f"DIAG:VMETER:MODE DC")
    if HP866xx.getvalue("DIAG:VMETER:MODE?") != "DC":
        print("Failed to set VMETER to DC")
    Vdc = float(HP866xx.getvalue("DIAG:VMETER?"))

    HP866xx.send(f"DIAG:VMETER:MODE AC")
    if HP866xx.getvalue("DIAG:VMETER:MODE?") != "AC":
        print("Failed to set VMETER to AC")
    Vac = float(HP866xx.getvalue("DIAG:VMETER?"))
    HP866xx.send('FM:STATE ON')
    print(f'{mux:>3d}  {Vdc:+7.3f}  {Vac:+7.3f}  {expected[i]:+7.3f}')

HP866xx.send('FM:STATE OFF')
HP866xx.send('FM:DEV 1kHz')
HP866xx.send('FM:SOURCE INT')
print("FM           : ", HP866xx.getvalue("FM:STATE?"))
print("FM deviation : ", HP866xx.getvalue("FM:DEV?"))
print("FM source    : ", HP866xx.getvalue("FM:SOURCE?"))

HP866xx.send('AM:FREQ 1kHz')
HP866xx.send('AM:DEPT 90%')
HP866xx.send('AM:SOURCE INT')
HP866xx.send('AM:STATE ON')
print("AM           : ", HP866xx.getvalue("AM:STATE?"))
print("AM depth     : ", HP866xx.getvalue("AM:DEPT?"))
print("AM frequency : ", HP866xx.getvalue("AM:FREQ?"))
print("AM source    : ", HP866xx.getvalue("AM:SOURCE?"))
for i in [2]:
    HP866xx.send(f"DIAG:LATCH:MUX {i:02d}")
    mux = int(HP866xx.getvalue("DIAG:LATCH:MUX?"))
    if mux != i:
        print(f"Failed to set MUX {i:d}")

    HP866xx.send(f"DIAG:VMETER:MODE DC")
    if HP866xx.getvalue("DIAG:VMETER:MODE?") != "DC":
        print("Failed to set VMETER to DC")
    Vdc = float(HP866xx.getvalue("DIAG:VMETER?"))

    HP866xx.send(f"DIAG:VMETER:MODE AC")
    if HP866xx.getvalue("DIAG:VMETER:MODE?") != "AC":
        print("Failed to set VMETER to AC")
    Vac = float(HP866xx.getvalue("DIAG:VMETER?"))
    print(f'{mux:>3d}  {Vdc:+7.3f}  {Vac:+7.3f}  {expected[i]:+7.3f}')



print("-----------------")
print("Reference A9 Test")
HP866xx.send('FREQ 3GHZ')
HP866xx.send('AMPL 7.5DBM')
HP866xx.send('AM:STATE OFF')
HP866xx.send('FM:STATE OFF')
HP866xx.send('AMPL:STATE ON')
print("Frequency    : ", HP866xx.getvalue("FREQ?"))
print("Synthesis    : ", HP866xx.getvalue("FREQ:SYNT?"))
print("Synth auto   : ", HP866xx.getvalue("FREQ:SYNT:AUTO?"))
print("Amplitude    : ", HP866xx.getvalue("AMPL?"))
print("RF           : ", HP866xx.getvalue("AMPL:STATE?"))
print("FM           : ", HP866xx.getvalue("FM:STATE?"))
print("AM           : ", HP866xx.getvalue("AM:STATE?"))

HP866xx.send('DIAG:LATCH:MOD 8')
print("Module tested : ", HP866xx.getvalue("DIAG:LATCH:MOD?"))
expected = [0.380,0.152,0.482,1.776,1.928,0,-3.578,0]
print('Mux     Vdc      Vac   Expected')
for i in range(8):
    HP866xx.send(f"DIAG:LATCH:MUX {i:02d}")
    mux = int(HP866xx.getvalue("DIAG:LATCH:MUX?"))
    if mux != i:
        print(f"Failed to set MUX {i:d}")

    HP866xx.send(f"DIAG:VMETER:MODE DC")
    if HP866xx.getvalue("DIAG:VMETER:MODE?") != "DC":
        print("Failed to set VMETER to DC")
    Vdc = float(HP866xx.getvalue("DIAG:VMETER?"))

    HP866xx.send(f"DIAG:VMETER:MODE AC")
    if HP866xx.getvalue("DIAG:VMETER:MODE?") != "AC":
        print("Failed to set VMETER to AC")
    Vac = float(HP866xx.getvalue("DIAG:VMETER?"))
    print(f'{mux:>3d}  {Vdc:+7.3f}  {Vac:+7.3f}  {expected[i]:+7.3f}')

print("-----------------")
print("HF Driver A8")
HP866xx.send('FREQ 1GHZ')
HP866xx.send('AMPL 10DBM')
HP866xx.send('AM:STATE OFF')
HP866xx.send('FM:STATE OFF')
HP866xx.send('AMPL:STATE ON')
print("Frequency    : ", HP866xx.getvalue("FREQ?"))
print("Synthesis    : ", HP866xx.getvalue("FREQ:SYNT?"))
print("Synth auto   : ", HP866xx.getvalue("FREQ:SYNT:AUTO?"))
print("Amplitude    : ", HP866xx.getvalue("AMPL?"))
print("RF           : ", HP866xx.getvalue("AMPL:STATE?"))
print("FM           : ", HP866xx.getvalue("FM:STATE?"))
print("AM           : ", HP866xx.getvalue("AM:STATE?"))

HP866xx.send('DIAG:LATCH:MOD 10')
print("Module tested : ", HP866xx.getvalue("DIAG:LATCH:MOD?"))
expected = [-0.55, 0.63, 0.05, 6.1, 4.1, 7.0, 0.02, 0.02]
print('Mux     Vdc      Vac   Expected')
for i in [0,1,2,3,4,5,6,7]:
    HP866xx.send(f"DIAG:LATCH:MUX {i:02d}")
    mux = int(HP866xx.getvalue("DIAG:LATCH:MUX?"))
    if mux != i:
        print(f"Failed to set MUX {i:d}")

    HP866xx.send(f"DIAG:VMETER:MODE DC")
    if HP866xx.getvalue("DIAG:VMETER:MODE?") != "DC":
        print("Failed to set VMETER to DC")
    Vdc = float(HP866xx.getvalue("DIAG:VMETER?"))

    HP866xx.send(f"DIAG:VMETER:MODE AC")
    if HP866xx.getvalue("DIAG:VMETER:MODE?") != "AC":
        print("Failed to set VMETER to AC")
    Vac = float(HP866xx.getvalue("DIAG:VMETER?"))
    print(f'{mux:>3d}  {Vdc:+7.3f}  {Vac:+7.3f}  {expected[i]:+7.3f}')
HP866xx.send('FREQ 187.5MHZ')
HP866xx.send('AMPL 10DBM')
print("Frequency    : ", HP866xx.getvalue("FREQ?"))
print("Amplitude    : ", HP866xx.getvalue("AMPL?"))
expected = [0, 0, 0, 0, 0, 0, 0.7, 1.5 ]
print('Mux     Vdc      Vac   Expected')
for i in [6,7]:
    HP866xx.send(f"DIAG:LATCH:MUX {i:02d}")
    mux = int(HP866xx.getvalue("DIAG:LATCH:MUX?"))
    if mux != i:
        print(f"Failed to set MUX {i:d}")

    HP866xx.send(f"DIAG:VMETER:MODE DC")
    if HP866xx.getvalue("DIAG:VMETER:MODE?") != "DC":
        print("Failed to set VMETER to DC")
    Vdc = float(HP866xx.getvalue("DIAG:VMETER?"))

    HP866xx.send(f"DIAG:VMETER:MODE AC")
    if HP866xx.getvalue("DIAG:VMETER:MODE?") != "AC":
        print("Failed to set VMETER to AC")
    Vac = float(HP866xx.getvalue("DIAG:VMETER?"))
    print(f'{mux:>3d}  {Vdc:+7.3f}  {Vac:+7.3f}  {expected[i]:+7.3f}')
HP866xx.send('FREQ 100.0MHZ')
HP866xx.send('AMPL -10DBM')
print("Frequency    : ", HP866xx.getvalue("FREQ?"))
print("Amplitude    : ", HP866xx.getvalue("AMPL?"))
expected = [0, 0, 0, 0, 0, 0, 0, 1.5 ]
print("Check printed value on HF Driver board")
print('Mux     Vdc      Vac   Expected')
for i in [7]:
    HP866xx.send(f"DIAG:LATCH:MUX {i:02d}")
    mux = int(HP866xx.getvalue("DIAG:LATCH:MUX?"))
    if mux != i:
        print(f"Failed to set MUX {i:d}")

    HP866xx.send(f"DIAG:VMETER:MODE DC")
    if HP866xx.getvalue("DIAG:VMETER:MODE?") != "DC":
        print("Failed to set VMETER to DC")
    Vdc = float(HP866xx.getvalue("DIAG:VMETER?"))

    HP866xx.send(f"DIAG:VMETER:MODE AC")
    if HP866xx.getvalue("DIAG:VMETER:MODE?") != "AC":
        print("Failed to set VMETER to AC")
    Vac = float(HP866xx.getvalue("DIAG:VMETER?"))
    print(f'{mux:>3d}  {Vdc:+7.3f}  {Vac:+7.3f}  {expected[i]:+7.3f}')



print("-----------------")
print("Reference A5 Test")
HP866xx.send('FREQ 188MHZ')
HP866xx.send('AMPL 10DBM')
HP866xx.send('AM:STATE OFF')
HP866xx.send('FM:STATE OFF')
HP866xx.send('AMPL:STATE ON')
print("Frequency    : ", HP866xx.getvalue("FREQ?"))
print("Synthesis    : ", HP866xx.getvalue("FREQ:SYNT?"))
print("Synth auto   : ", HP866xx.getvalue("FREQ:SYNT:AUTO?"))
print("Amplitude    : ", HP866xx.getvalue("AMPL?"))
print("RF           : ", HP866xx.getvalue("AMPL:STATE?"))
print("FM           : ", HP866xx.getvalue("FM:STATE?"))
print("AM           : ", HP866xx.getvalue("AM:STATE?"))

HP866xx.send('DIAG:LATCH:MOD 11')
print("Module tested : ", HP866xx.getvalue("DIAG:LATCH:MOD?"))
expected = [-0.3,0.18,0.25,-1.88,2.66,0,0,0]
print('Mux     Vdc      Vac   Expected')
for i in [0,1,2,3,4,5,6,7]:
    HP866xx.send(f"DIAG:LATCH:MUX {i:02d}")
    mux = int(HP866xx.getvalue("DIAG:LATCH:MUX?"))
    if mux != i:
        print(f"Failed to set MUX {i:d}")

    HP866xx.send(f"DIAG:VMETER:MODE DC")
    if HP866xx.getvalue("DIAG:VMETER:MODE?") != "DC":
        print("Failed to set VMETER to DC")
    Vdc = float(HP866xx.getvalue("DIAG:VMETER?"))

    HP866xx.send(f"DIAG:VMETER:MODE AC")
    if HP866xx.getvalue("DIAG:VMETER:MODE?") != "AC":
        print("Failed to set VMETER to AC")
    Vac = float(HP866xx.getvalue("DIAG:VMETER?"))
    print(f'{mux:>3d}  {Vdc:+7.3f}  {Vac:+7.3f}  {expected[i]:+7.3f}')
HP866xx.send('FREQ 100MHZ')
HP866xx.send('AMPL 10DBM')
print("Frequency    : ", HP866xx.getvalue("FREQ?"))
print("Amplitude    : ", HP866xx.getvalue("AMPL?"))
print('Mux     Vdc      Vac   Expected')
expected = [0,-2.36,0.1]
for i in [1,2]:
    HP866xx.send(f"DIAG:LATCH:MUX {i:02d}")
    mux = int(HP866xx.getvalue("DIAG:LATCH:MUX?"))
    if mux != i:
        print(f"Failed to set MUX {i:d}")

    HP866xx.send(f"DIAG:VMETER:MODE DC")
    if HP866xx.getvalue("DIAG:VMETER:MODE?") != "DC":
        print("Failed to set VMETER to DC")
    Vdc = float(HP866xx.getvalue("DIAG:VMETER?"))

    HP866xx.send(f"DIAG:VMETER:MODE AC")
    if HP866xx.getvalue("DIAG:VMETER:MODE?") != "AC":
        print("Failed to set VMETER to AC")
    Vac = float(HP866xx.getvalue("DIAG:VMETER?"))
    print(f'{mux:>3d}  {Vdc:+7.3f}  {Vac:+7.3f}  {expected[i]:+7.3f}')

HP866xx.send("*RST")
HP866xx.close()
