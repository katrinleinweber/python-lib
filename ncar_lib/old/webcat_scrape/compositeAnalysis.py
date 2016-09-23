import os, sys, traceback
from JloXml import XmlUtils, XmlRecord

path = 'WebCatCompositeData/NCAR Technical Notes/1.xml'

# rec = XmlRecord (path=path)

	
class Record (XmlRecord):
	
	def getTagNames (self):
		# print self
		tags = []
		children = XmlUtils.getChildElements (self.doc)
		for child in children:
			# print "*", child.tagName
			if not child.tagName in tags:
				tags.append (child.tagName)
		return tags
				
class Directory:
	
	def __init__ (self, path):
		self.path = path
		self.tags = []
		
		for filename in os.listdir(path):
			if filename[0] == '.':
				continue
			recpath = os.path.join (self.path, filename)
			# print recpath
			rec = Record (path=recpath)
			# print rec
			for tag in rec.getTagNames():
				# print tag
				if not tag in self.tags:
					self.tags.append (tag)
					
		print "TAGS"
		for tag in self.tags:
			print "\t", tag
			
def main():
	Directory ('WebCatCompositeData/NCAR Technical Notes')
	Directory ('WebCatCompositeData/Monographs')
	Directory ('WebCatCompositeData/NCAR Manuscripts')		
	
def recTester ():
	path = 'WebCatCompositeData/NCAR Manuscripts/flooberry.xml'
	rec = Record (path=path)
	for tag in rec.getTagNames():
		print tag
if __name__ == '__main__':
	main()
	# recTester()