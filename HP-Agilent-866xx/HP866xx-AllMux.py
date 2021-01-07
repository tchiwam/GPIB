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

for i in range(64):
    HP866xx.send(f'DIAG:LATCH:MOD {i:d}')
    module = int(HP866xx.getvalue("DIAG:LATCH:MOD?"))
    if module == i:
        print("Module tested : ", module)
        for j in range(32):
            HP866xx.send(f"DIAG:LATCH:MUX {j:d}")
            mux = int(HP866xx.getvalue("DIAG:LATCH:MUX?"))
            if mux == i:
                HP866xx.send(f"DIAG:VMETER:MODE DC")
                if HP866xx.getvalue("DIAG:VMETER:MODE?") != "DC":
                    print("Failed to set VMETER to DC")
                Vdc = float(HP866xx.getvalue("DIAG:VMETER?"))
                HP866xx.send(f"DIAG:VMETER:MODE AC")
                if HP866xx.getvalue("DIAG:VMETER:MODE?") != "AC":
                    print("Failed to set VMETER to AC")
                Vac = float(HP866xx.getvalue("DIAG:VMETER?"))
                print("Mux ",j,"=",Vdc,"VDC ",Vac,"VAC  ")
    print()
HP866xx.send("*RST")
HP866xx.close()
