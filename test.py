import mysetup
import znacky

m=mysetup.setup()
m.save()
#print znacky.znackyToTeX (m.znacky)
print(znacky.znackyToTB (m.znacky).obdelnik)
znacky.znackyToTB (m.znacky).GV ()
