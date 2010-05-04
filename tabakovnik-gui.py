#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygtk
pygtk.require('2.0')
import gtk
import gettextdialog

import mysetup
import znacky

(
    Z_COLUMN_NAZEV,
    Z_COLUMN_CENA,
) = range(2)
(
    T_COLUMN_NAZEV,
    T_COLUMN_JE,
) = range(2)
class Znackovnik:
	def __init__(self, ):
		self.radky = 3
		self.setup = mysetup.setup()
		self.hBox = gtk.HBox()
		self.Z_listStore = gtk.ListStore (str, int) #UPDATE ON COLUMN CHANGE
		self.Z_treeView = gtk.TreeView (self.Z_listStore)
		self.Z_nazevCell = gtk.CellRendererText ()
		self.Z_nazevColumn = gtk.TreeViewColumn ('Nazev', self.Z_nazevCell, text=Z_COLUMN_NAZEV)
		self.Z_cenaCell = gtk.CellRendererText ()
		self.Z_cenaColumn = gtk.TreeViewColumn ('Cena', self.Z_cenaCell, text=Z_COLUMN_CENA)
		self.Z_treeView.append_column (self.Z_nazevColumn)
		self.Z_treeView.append_column (self.Z_cenaColumn)
		self.Z_treeScroll = gtk.ScrolledWindow()
		self.Z_treeScroll.add (self.Z_treeView)
		self.Z_treeScroll.set_policy (gtk.POLICY_NEVER, gtk.POLICY_NEVER)
		self.Z_treeScroll.set_policy (gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)
		self.Z_treeView.connect ("cursor-changed", self.ZChanged)

		self.hBox.pack_start (self.Z_treeScroll)

		self.T_listStore = gtk.ListStore (str, 'gboolean') #UPDATE ON COLUMN CHANGE
		self.T_treeView = gtk.TreeView (self.T_listStore)
		self.T_nazevCell = gtk.CellRendererText ()
		self.T_nazevColumn = gtk.TreeViewColumn ('Nazev', self.T_nazevCell, text=T_COLUMN_NAZEV)
		self.T_cenaCell = gtk.CellRendererToggle ()
		self.T_cenaColumn = gtk.TreeViewColumn ('Je', self.T_cenaCell, active=T_COLUMN_JE)
		self.T_treeView.append_column (self.T_nazevColumn)
		self.T_treeView.append_column (self.T_cenaColumn)
		self.T_treeScroll = gtk.ScrolledWindow()
		self.T_treeScroll.add (self.T_treeView)
		self.T_treeScroll.set_policy (gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)
		self.T_treeView.connect ("row-activated", self.TActivated)

		self.hBox.pack_start (self.T_treeScroll)
		self.hBoxBut = gtk.HBox ()
		self.BAdd = gtk.Button (u'_Přidat tabák')
		self.BAdd.connect ('clicked', self.onAdd)
		self.hBoxBut.add (self.BAdd)
		self.BPreview = gtk.Button (u'_Náhled')
		self.BPreview.connect ('clicked', self.onPreview)
		self.hBoxBut.add (self.BPreview)
		self.BPrint = gtk.Button (u'_Tisk')
		self.BPrint.connect ('clicked', self.onPrint)
		self.hBoxBut.add (self.BPrint)

		self.vBox = gtk.VBox ()
		self.vBox.add (self.hBox)
		self.vBox.pack_start(self.hBoxBut, False, False, 2)

		self.widget = gtk.Frame()
		self.widget.add (self.vBox)
		
		self.RepopulateZ ()
	def Radky (self, radky):
		self.radky = radky
		print 'baf'+str(radky)
	def onAdd (self, widget):
		nazev = gettextdialog.getText('<b>Přidání nového tabáku</b>', 'název:')
		self.aZnacka.addTabak (znacky.tabak(nazev, 'ano'))
		self.RepopulateT ()
	def onPreview (self, widget):
		znacky.znackyToTB (self.setup.znacky, self.radky).GV('gv')
	def onPrint (self, widget):
		znacky.znackyToTB (self.setup.znacky, self.radky).GV('lpr')
		
	def RepopulateZ (self):
		self.Z_listStore.clear()
		for z in self.setup.znacky:
			rowiter = self.Z_listStore.append (row=None)
			self.Z_listStore.set_value (rowiter, Z_COLUMN_CENA, int(z.cena))
			self.Z_listStore.set_value (rowiter, Z_COLUMN_NAZEV, z.nazev)
	def TActivated (self, treeview, path, column):
		(model, iter) = self.T_treeView.get_selection().get_selected()
		if iter is None:
			return None
		nazev, = model.get (iter, T_COLUMN_NAZEV)
		for t in self.aZnacka.tabaky:
			if t.nazev == nazev:
				if t.je == 'ano':
					t.je = 'ne'
					model.set (iter, T_COLUMN_JE, False)
				else:
					t.je = 'ano'
					model.set (iter, T_COLUMN_JE, True)
	def ZChanged (self, treeview):
		(model, iter) = self.Z_treeView.get_selection().get_selected()
		if iter is None:
			return None
		nazev, = model.get (iter, Z_COLUMN_NAZEV)
		for z in self.setup.znacky:
			if z.nazev == nazev:
				self.aZnacka = z
		self.RepopulateT ()
	def RepopulateT (self):
		self.T_listStore.clear()
		for t in self.aZnacka.tabaky:
			rowiter = self.T_listStore.append (row=None)
			self.T_listStore.set_value (rowiter, T_COLUMN_JE, t.je=='ano')
			self.T_listStore.set_value (rowiter, T_COLUMN_NAZEV, t.nazev)


class Tabakovnik:
	def onSave(self, widget, data=None):
		self.setup.save()
	def destroy(self, widget, data=None):
		gtk.main_quit()
	def __init__(self):
		self.radku = 3
		self.setup = mysetup.setup()
		self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
		self.window.set_title('Tabakovnik')
		self.window.connect("destroy", self.destroy)
		self.VBox = gtk.VBox()
		self.window.add (self.VBox)

		menu_bar = gtk.MenuBar()
		self.VBox.pack_start(menu_bar, False, False, 2)

		file_menu_i = gtk.MenuItem("_File")
		menu_bar.append (file_menu_i)
		file_menu = gtk.Menu()
		it = gtk.MenuItem('S_ave')
		file_menu.append (it)
		it.connect("activate", self.onSave)
		it = gtk.MenuItem('E_xit')
		file_menu.append (it)
		it.connect("activate", self.destroy)
		file_menu_i.set_submenu (file_menu)

		self.znackovnik = Znackovnik ()
		self.RHBox = gtk.HBox ()
		RadioRIII = gtk.RadioButton (None, "3 radky")
		RadioRIII.connect("clicked", self.OnRadkyIII)
		self.RHBox.add (RadioRIII)
		RadioRII = gtk.RadioButton (RadioRIII, "2 radky")
		RadioRII.connect("clicked", self.OnRadkyII)
		self.RHBox.add (RadioRII)
		self.VBox.pack_start (self.RHBox, False, False)
		self.VBox.add (self.znackovnik.widget)


		self.window.show_all()
	def OnRadkyIII (self, widget, data=None):
		self.znackovnik.Radky (3)
	def OnRadkyII (self, widget, data=None):
		self.znackovnik.Radky (2)
	def main(self):
		gtk.main()

if __name__ == "__main__":
	tabakovnik = Tabakovnik()
	tabakovnik.main()
