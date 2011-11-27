import texbuilder
import texbuilder2
import locale

class tabak:
	def __init__(self, nazev="", je=""):
		self.nazev = nazev
		self.je = je
	def toElement (self, dom):
		elem = dom.createElement ('tabak')
		elem.setAttribute ("nazev", str(self.nazev))
		elem.setAttribute ("je", str(self.je))
		return elem
	def toTeX (self, tb):
		tb.Tabak (self.nazev)

def tabakFromElement (elem):
	nazev = ""
	je = ""
	if (elem.hasAttribute ("nazev")):
		nazev = elem.getAttribute ("nazev")
	if (elem.hasAttribute ("je")):
		je = elem.getAttribute ("je")
	return tabak (nazev=nazev, je=je)
	
class znacka:
	def __init__(self, nazev="", cena=0):
		self.tabaky = []
		self.nazev = nazev
		self.cena = cena
	def addTabak (self, tabak):
		def TabakyCompare (x, y):
			return locale.strcoll(x.nazev, y.nazev)
		self.tabaky.append (tabak)
		self.tabaky.sort (TabakyCompare)
	def toElement (self, dom):
		elem = dom.createElement ('znacka')
		elem.setAttribute ("nazev", str(self.nazev))
		elem.setAttribute ("cena", str(self.cena))
		for t in self.tabaky:
			elem.appendChild (t.toElement (dom))
		return elem
	def toTeX (self, tb):
		count = 0
		for t in self.tabaky:
			if t.je == "ano":
				count += 1
		if count == 0:
			return
		tb.Znacka (self.nazev, self.cena)
		tb.BPrvniSloupec ()
		i = 0
		sl = False
		for t in self.tabaky:
			if t.je == "ano":
				if i+1 > (count+count%2)/2. and not sl:
					tb.EPrvniBDruhySloupec ()
					sl = True
				t.toTeX(tb)
				i += 1
		tb.EDruhySloupec ()
	def toTeXX (self, tb):
		count = 0
		tb.Znacka (self.nazev, self.cena)
		tb.BPrvniSloupec ()
		for t in self.tabaky:
			t.toTeX(tb)

def znackaFromElement (elem):
	nazev="Noname"
	cena = 0
	if (elem.hasAttribute ("nazev")):
		nazev = elem.getAttribute ("nazev")
	if (elem.hasAttribute ("cena")):
		cena = elem.getAttribute ("cena")
	znack = znacka(nazev=nazev, cena=cena)
	elemsTabaky = elem.getElementsByTagName("tabak")
	for elementTabak in elemsTabaky:
		ty = tabakFromElement (elementTabak)
		znack.addTabak (ty)
	return znack

def znackyFromElement (elem):
	znacky = []
	elemsZnacky = elem.getElementsByTagName("znacka")
	for elementZnack in elemsZnacky:
		ty = znackaFromElement (elementZnack)
		znacky.append (ty)
	return znacky

def znackyToTB (znacky, radky):
	tb = texbuilder.TeXBuilder (radku=radky)
	tb.BeginObdelnik ()
	for z in znacky:
		z.toTeX (tb)
	return tb

def znackyToTBX (znacky):
	tb = texbuilder2.TeXBuilderX ()
	tb.BeginObdelnik ()
	for z in znacky:
		z.toTeXX (tb)
		tb.poZnacce()
	return tb
