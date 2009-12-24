import texbuilder
import locale

class tabak:
	def __init__(self, nazev="", je=""):
		self.nazev = nazev
		self.je = je
	def toElement (self, dom):
		elem = dom.createElement ('tabak')
		elem.setAttribute ("nazev", unicode(self.nazev))
		elem.setAttribute ("je", unicode(self.je))
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
		elem = dom.createElement (u'znacka')
		elem.setAttribute (u"nazev", unicode(self.nazev))
		elem.setAttribute (u"cena", unicode(self.cena))
		for t in self.tabaky:
			elem.appendChild (t.toElement (dom))
		return elem
	def toTeX (self, tb):
		count = 0
		for t in self.tabaky:
			if t.je == u"ano":
				count += 1
		if count == 0:
			return
		tb.Znacka (self.nazev, self.cena)
		tb.BPrvniSloupec ()
		i = 0
		sl = False
		for t in self.tabaky:
			if t.je == u"ano":
				if i+1 > (count+count%2)/2. and not sl:
					tb.EPrvniBDruhySloupec ()
					sl = True
				t.toTeX(tb)
				i += 1
		tb.EDruhySloupec ()

def znackaFromElement (elem):
	nazev=u"Noname"
	cena = 0
	if (elem.hasAttribute (u"nazev")):
		nazev = elem.getAttribute (u"nazev")
	if (elem.hasAttribute (u"cena")):
		cena = elem.getAttribute (u"cena")
	znack = znacka(nazev=nazev, cena=cena)
	elemsTabaky = elem.getElementsByTagName(u"tabak")
	for elementTabak in elemsTabaky:
		ty = tabakFromElement (elementTabak)
		znack.addTabak (ty)
	return znack

def znackyFromElement (elem):
	znacky = []
	elemsZnacky = elem.getElementsByTagName(u"znacka")
	for elementZnack in elemsZnacky:
		ty = znackaFromElement (elementZnack)
		znacky.append (ty)
	return znacky

def znackyToTB (znacky):
	tb = texbuilder.TeXBuilder ()
	tb.BeginObdelnik ()
	for z in znacky:
		z.toTeX (tb)
	return tb

