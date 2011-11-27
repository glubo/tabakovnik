# -*- coding: utf-8 -*-
import codecs
import os
import tempfile
import shutil

TDocStart = '''
%pdfcsplaintex
\\advance\\vsize 1.5cm
\\advance\\voffset -1cm
\\advance\\hsize 3cm
\\advance\\hoffset -1.5cm
\\font\\fnadp=cscsc10
\\font\\fsnadp=cscsc10
\\font\\fcaj=csss10
\\def\\vertikalovac{}
\\def\\horizantovac{\\hrule}
{\\catcode`*=13\\gdef*{\\cr}}
{\\catcode`|=13\\gdef|{\\gdef\\vertikalovac{\\vrule}}}
\\def\\vvrule{\\vertikalovac\\gdef\\vertikalovac{}}
\\def\\hhrule{\\horizantovac\\gdef\\horizantovac{\\hrule}}
\\def\\hr{\\noalign{\\hhrule}}
\\def\\zmizni#1{\\relax}

\\def\\zacatektab{\\bigskip\\line\\bgroup\\hfil\\vbox\\bgroup\\catcode9=4\\endlinechar=`*\\catcode`*=13\\catcode`|=13%
\\halign\\bgroup\\strut\\vrule\\quad\\hfil##\\quad\\vvrule&&\\quad\\hfil##\\quad\\strut\\vvrule\\cr%
\\noalign{\\hrule}%
}
\\def\\konectab{\\hr\\egroup\\egroup\\hfil\\egroup\\zmizni
}
\\def\\datum{&\\hskip 1em\\noexpand\\gdef\\vertikalovac{\\vrule}}
\\def\\kazdyradek{\\datum\\datum\\datum\\datum\\datum\\datum\\datum\\datum\\datum\\datum\\datum\\datum\\datum}
\\def\\znacka#1{\\hr\\fnadp #1\\kazdyradek\\gdef\\horizantovac{\\hrule height2px}}
\\def\\tabak#1{\\hr\\fcaj #1\\kazdyradek\\gdef\\horizantovac{\\hrule height0.6px}}
\\def\\tabakk#1{\\hr\\fcaj #1\\kazdyradek\\gdef\\horizantovac{\\hrule height0.9px}}
\\zacatektab
data:\kazdyradek
'''.decode('utf-8')

TDocEnd = '''
\\konectab
\\bye
'''.decode('utf-8')

class TeXBuilderX:
	def __init__ (self):
		self.obdelnik = u''
		self.radku = 0
		
	def BeginObdelnik (self):
		self.obdelnik = u''
	
	def Znacka (self, nazev, cena):
		self.obdelnik += u'\\konectab\n\\vfill\n\\zacatektab\n\\znacka{'+unicode(nazev)+"}\n"
	def BPrvniSloupec (self):
		pass
	def EPrvniBDruhySloupec (self):
		pass
	def EDruhySloupec (self):
		pass
	def Tabak (self, nazev):
		self.radku += 1
		if self.radku %2:
			self.obdelnik += u'\\tabak{'+unicode(nazev)+'}\n'
		else:
			self.obdelnik += u'\\tabakk{'+unicode(nazev)+'}\n'
	def poZnacce (self):
		self.obdelnik += u'\\tabak{}\n\\tabak{}\n'
	
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

