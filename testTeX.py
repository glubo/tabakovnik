import texbuilder
import os
import codecs
import tempfile
import shutil

t = texbuilder.TeXBuilder ()
t.BeginObdelnik()
t.Znacka ('Nakhla', 90)
t.BPrvniSloupec()
t.Tabak('a')
t.Tabak('a')
t.EPrvniBDruhySloupec()
t.Tabak('b')
t.EDruhySloupec()
t.Znacka ('Waha', 90)
t.BPrvniSloupec()
t.Tabak('a')
t.EPrvniBDruhySloupec()
t.Tabak('b')
t.EDruhySloupec()

t.GV ()
