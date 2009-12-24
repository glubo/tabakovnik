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
\\def\\znacka#1#2{\\vtop {\\vskip 3pt \\hrule\\vskip 3pt \\hbox to \\wsloupec {\\fnadp #1 \\hfill #2 Kč\\hskip 1em}\\vskip 2pt\\hrule}}
\\long\\def\\sloupecek#1{\\hbox to \\wsloupecek{\\vtop{#1}}}
\\def\\tabak#1{\\hbox to \\wsloupecek {#1\\hfil}}


\\def\\obdelnik {
\\vbox  {
'''.decode('utf-8')

TDocEnd = '''
\\vskip 6pt
\\vfil
}
}
\\def\\radek{\\hbox to \\hsize {\\obvod{\\vbox to 0.3\\vsize{\\vskip 0pt plus 0.2fil \\hbox to 0.49\\hsize{\\hfil\\obdelnik\\hfil}\\vfil}}\\obvod{\\vbox to 0.3\\vsize{\\vskip 0pt plus 0.2fil \\hbox to 0.49\\hsize{\\hfil\\obdelnik\\hfil}\\vfil}}\\hfil}}
\\radek
\\radek
\\radek
\\bye
'''.decode('utf-8')

class TeXBuilder:
	def __init__ (self):
		self.obdelnik = u''
		
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
		f.write(unicode (TDocStart+ self.obdelnik + TDocEnd).encode('UTF-8'))# )
		f.close ()

		os.spawnlp(os.P_WAIT, 'iconv', 'iconv', '-f','UTF-8', '-t', 'ISO8859-2', '-o', 't.tex', 'testTeXo.tex')
		os.spawnlp(os.P_WAIT, 'mv', 'mv', 't.tex', 'testTeXo.tex')
		os.spawnlp(os.P_WAIT, 'pdfcsplain', 'pdfcsplain', 'testTeXo.tex')
		os.spawnlp(os.P_WAIT, action, action, 'testTeXo.pdf')
		os.chdir (ocwd)
		shutil.rmtree (tempdir)
	def Print (self):
		tempdir = tempfile.mkdtemp()
		ocwd = os.getcwd ()
		os.chdir (tempdir)
		f = open ('testTeXo.tex', 'w')
		f.write(unicode (TDocStart+ self.obdelnik + TDocEnd).encode('UTF-8'))# )
		f.close ()

		os.spawnlp(os.P_WAIT, 'iconv', 'iconv', '-f','UTF-8', '-t', 'ISO8859-2', '-o', 't.tex', 'testTeXo.tex')
		os.spawnlp(os.P_WAIT, 'mv', 'mv', 't.tex', 'testTeXo.tex')
		os.spawnlp(os.P_WAIT, 'pdfcsplain', 'pdfcsplain', 'testTeXo.tex')
		os.spawnlp(os.P_WAIT, 'lpr', 'lpr', 'testTeXo.pdf')
		os.chdir (ocwd)
		shutil.rmtree (tempdir)

