import matplotlib.pyplot as plt
from matplotlib import colors

from gpibeth import gpibeth
from time import sleep

GPIBHOST = "172.20.0.50"
GPIBPORT = 1234
GPIBADDR = 2

gpib = gpibeth(GPIBHOST,GPIBPORT,GPIBADDR)
#gpib.setverbose(True)

print("Prologix Ethernet version: ", gpib.getvalue("++ver"))

gpib.send("IP;")
err = gpib.getvalue("ERR?;")
print(err)



print(gpib.getvalue("DONE?"))



gpib.settimeout(30)
data = list(map(int,gpib.getvalue("CURV?",eol=0x0a).split(",")))
print(data)
gpib.close()

plt.plot(data)
plt.title("Channel 1")
plt.suptitle("samples")
plt.xlabel("Sample #")
plt.ylabel("Value")
plt.show()

