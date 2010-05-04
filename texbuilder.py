# -*- coding: utf-8 -*-
import codecs
import os
import tempfile
import shutil

TDocStart = '''
%pdfcsplaintex
\\newdimen\\wsloupec
\\newdimen\\wsloupecek
\\advance\\vsize 1.5cm
\\advance\\voffset -1cm
\\advance\\hsize 3cm
\\advance\\hoffset -1.5cm
\\font\\fnadp=cscsc12
\\font\\fsnadp=cscsc10
\\font\\fcaj=cscsc12


\\wsloupec=0.4\\hsize
\\wsloupecek=0.48\\wsloupec
\\long\\def\\obvod #1{\\vbox{\\hrule \\hbox{\\vrule #1\\vrule}\\hrule}}
\\def\\caj#1#2{\\hbox to \\wsloupec {\\fcaj#1\\leaders\\hbox{.}\\hfil#2 Kč}}
\\def\\popis#1{\\hbox to \\wsloupec {\\it (#1)\\hfill}}
\\def\\znacka#1#2{\\vtop {\\vskip 3pt \\hrule\\vskip 2pt \\hbox to \\wsloupec {\\hskip 0.5em\\fnadp #1 \\hfill #2 Kč\\hskip 1em}\\vskip 2pt\\hrule}}
\\long\\def\\sloupecek#1{\\hskip 0.2em\\hbox to \\wsloupecek{\\vtop{\\baselineskip=0.0em#1}}\\hfil}
\\def\\tabak#1{\\hbox to \\wsloupecek {\\vphantom{ČŽŘpj}#1\\hfil}\\vskip-2pt}


\\def\\obdelnik {
\\vbox  {
\\vskip 2pt
\\hbox to \\wsloupec {\\fnadp Všechny dýmky jsou od 18-ti let\\hfil}\\vskip -1em
'''.decode('utf-8')

TDocEnd_III = '''
\\vskip 6pt
\\vfil
}
}
\\def\\radek{\\hbox to \\hsize {\\obvod{\\vbox to 0.3\\vsize{\\vskip 0pt plus 0.2fil \\hbox to 0.49\\hsize{\\hfil\\obdelnik\\hfil}\\vfil}}\\obvod{\\vbox to 0.3\\vsize{\\vskip 0pt plus 0.2fil \\hbox to 0.49\\hsize{\\hfil\\obdelnik\\hfil}\\vfil}}\\hfil}}
\\radek
\\vskip-1pt
\\radek
\\vskip-1pt
\\radek
\\bye
'''.decode('utf-8')
TDocEnd_II = '''
\\vskip 6pt
\\vfil
}
}
\\def\\radek{\\hbox to \\hsize {\\obvod{\\vbox to 0.48\\vsize{\\vskip 0pt plus 0.2fil \\hbox to 0.49\\hsize{\\hfil\\obdelnik\\hfil}\\vfil}}\\obvod{\\vbox to 0.48\\vsize{\\vskip 0pt plus 0.2fil \\hbox to 0.49\\hsize{\\hfil\\obdelnik\\hfil}\\vfil}}\\hfil}}
\\radek
\\vskip-1pt
\\radek
\\bye
'''.decode('utf-8')

class TeXBuilder:
	def __init__ (self, radku=3):
		self.obdelnik = u''
		self.radku = radku
		
	def BeginObdelnik (self):
		self.obdelnik = u''
	
	def Znacka (self, nazev, cena):
		self.obdelnik += u'\\znacka{'+unicode(nazev)+'}{'+unicode(cena)+u"}\n"
	def BPrvniSloupec (self):
		self.obdelnik += u'\\hbox to \\wsloupec { \sloupecek {\n'
	def EPrvniBDruhySloupec (self):
		self.obdelnik += u'}\\sloupecek{\n'
	def EDruhySloupec (self):
		self.obdelnik += u'}\\hfil}\n'
	def Tabak (self, nazev):
		self.obdelnik += u'\\tabak{'+unicode(nazev)+'}\n'
	
	def GV (self, action='gv'):
		tempdir = tempfile.mkdtemp()
		ocwd = os.getcwd ()
		os.chdir (tempdir)
		f = open ('testTeXo.tex', 'w')
		if self.radku == 3:
			f.write(unicode (TDocStart+ self.obdelnik + TDocEnd_III).encode('UTF-8'))
		elif self.radku == 2:
			f.write(unicode (TDocStart+ self.obdelnik + TDocEnd_II).encode('UTF-8'))
		
		f.close ()

		os.spawnlp(os.P_WAIT, 'iconv', 'iconv', '-f','UTF-8', '-t', 'ISO8859-2', '-o', 't.tex', 'testTeXo.tex')
		os.spawnlp(os.P_WAIT, 'mv', 'mv', 't.tex', 'testTeXo.tex')
		os.spawnlp(os.P_WAIT, 'pdfcsplain', 'pdfcsplain', 'testTeXo.tex')
		os.spawnlp(os.P_WAIT, action, action, 'testTeXo.pdf')
		os.chdir (ocwd)
		shutil.rmtree (tempdir)
	def Print (self):
		self.GV (action="lpr")

