import znacky

from xml.dom import minidom

class setup:
	__shared_state = {}
	def __init__ (self, path = 'config.xml'):
		self.__dict__ = self.__shared_state
		if not hasattr (self, 'znacky'):
			self.path = path
			self.reload ()

	def reload (self):
		file = open (self.path, 'r')
		dom = minidom.parse (file)
		file.close ()


		e = dom.getElementsByTagName("znacky")
		self.znacky = znacky.znackyFromElement (e[0])


	def save (self):
		dom = minidom.getDOMImplementation ().createDocument (None, 'tabakovnik', None)
		elem = dom.createElement ('znacky')
		dom.firstChild.appendChild(elem)
		for znacka in self.znacky:
			elem.appendChild (znacka.toElement (dom))
		file = open (self.path, 'w')
		file.write (dom.toprettyxml (encoding='UTF-8'))
		file.close ()
		
