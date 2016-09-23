import os, sys, string

from AsnRecord import *
from HyperText.HTML40 import *
from HtmlDocument import MyDocument
from StdDocument import StdDocument
from AsnStandard import AsnStandard, AsnStandardHtml
from util import *
import AsnGlobals

class StdDocumentHtml (StdDocument):

	stdConstructor = AsnStandardHtml
	template = "html/StandardsTemplate.html"

	def __init__ (self, path, baseId=None):
		StdDocument.__init__ (self, path)
		self.baseId = baseId
		baseStd = self.root

		if baseId is not None:
			baseStd = self[makeFullId (baseId)]

		self.filename = os.path.split(path)[1]
		# print "ASN Standards Doc with " + self.filename
		self.html = DIV ()
		self.html.append (DIV (B("Source File: "), self.filename, klass="std-file"))
		self.html.append (DIV (B("File Created: "), self.fileCreated, klass="std-file"))
		
		self.html.append (self.toolBar())
		
		hierarchy = DIV (klass="hierarchy")
		self.html.append (hierarchy )
		
		# standards = DIV(klass="box-"+str(baseStd.level))
		# self.html.append (standards) 
		self._makeHtml (baseStd, hierarchy, baseStd.level)
	
	def rootToHtml (self):
		rootHtml = DIV (id="root")
		rootHtml.append (DIV (self.title.encode ("utf8", "replace"), klass="doc-title"))
		rootHtml.append (DIV (self.root.description.encode("utf8", "replace"), klass="doc-description"))
		return rootHtml
		
	def _makeHtml (self, baseStd, parent, level=0, maxlevels=10):
		"""
		recursively traverse the standards tree, building a hierarchical
		html representation

		the html for the individual nodes is generated by the "baseStd.toHtml" call
		"""
		debug = 0;
		strict = 0;
		
		if level > maxlevels:
			return
			
		if debug:
			if baseStd is None:
				print "ERROR: baseStd is None!"
				return
			else:
				print "%s*baseStd: %s" % ("   "*level, baseStd.id)
			
		# render the std (<node><node-control/><node-text/></node>
		if baseStd == self.root:
			stdNode = self.rootToHtml()
		else:
			stdNode = baseStd.toHtml ()
			
		parent.append (stdNode)
			
		if (baseStd.children):
			if debug: print "\n%sprocessing %d children" % ("   "*level, len(baseStd.children))
			
			if level == -1:
				boxClass = "box root-level"
			else:
				boxClass = "box level-"+str(level)
			
			childrenBox = DIV (klass=boxClass, style="display:block")
			
			stdNode.append (childrenBox)
			children = baseStd.children
			children.sort (self.childCmp)
			for std in children:
				if debug: print "%s-child: %s" % ("   "*level, std)
				node = self[std]
				if node is None:
					## this shouldn't happen! 
					if strict:
						raise Exception, "Undefined Standard Node: %s" % std
					else:
						print "WARNING: Undefined Standard Node: %s" % std
						continue  # makeHtml will choke if we don't return here
				self._makeHtml (self[std], childrenBox, level+1, maxlevels)

	def toHtml (self):
		return self.html

	def _sortVal (self, s):
		try:
			val = float (s.split(" ")[0])
		except:
			val = s
		# self.show_sortVal (s, val)
		return val
		
	def show_sortVal (self, s, v):
		print "%s\n\t%s (%s)" % (s, v, type(v))
				
	def childCmp (self, c1, c2):
		"""
		sort by gradeRange first, description second
		"""
		std1 = self[c1]
		std2 = self[c2]
		try:
			grCmp = gradeRangeCmp (std1.gradeRange, std2.gradeRange)
			if grCmp == 0:
				return cmp (self._sortVal(std1.description), self._sortVal(std2.description))
			else:
				return grCmp
		except:
			## print "sort is punting"
			return 0
		
	def toolBar(self):
		
		exposer = DIV ("open to level: ")
		for i in range(self.levels+1):
			value = " %d " % (i+1)
			onclick = "exposeToLevel(%d)" % (i)
			exposer.append (INPUT (type="button", klass="tool-bar-button", value=value, onclick=onclick))
	  	#search <input id="search-str" type="text" /> 
		# <input id="search-button" type="button" value=" go "/>
		
		searchBox = INPUT (type="text", id="search-str")
		searchButton = INPUT (type="button", id="search-button", value=" go ");
		searcher = DIV ("search (id#): %s %s" % (searchBox, searchButton))
		
		return FORM (TABLE (TR (TD (exposer), TD (searcher)), klass="tool-bar"),
			id="tool-bar-form")
		
		
	def makeHtmlDoc (self):
		"""
		Generate the html document as string
		"""
		## title = os.path.splitext(self.filename)[0]
		title=self.title
		doc = MyDocument (title=title, stylesheet="styles.css")
		# doc.body["onload"] = "init();"
		
		# <meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1">
		
		doc.head.append (META(http_equiv="Content-Type",
                          content="text/html; charset=utf-8"))
		
		doc.addJavascript ("javascript/prototype.js")
		doc.addJavascript ("javascript/asn-scripts.js")
		doc.append (DIV (id="stats-overlay"))
		doc.append (DIV (id="debug"))
		doc.append (H1 (title))
		
		doc.append (self.html)
		return doc
		
	def write (self, path):
		# f = open (path, 'w')
		self.makeHtmlDoc().writeto (path)

		print "html written to ", path

def makeEarthScienceStandards ():
	os.path.join (AsnGlobals.sourceDir, "1996-New-York-Science-localized.xml")

	# Earth Science standards
	asn = StdDocumentHtml (path,"S102A818")

	outPath = "html/ASN-New-York-Earth-Science.html"
	asn.write (outPath)
	
	
def makeStandardsHtml (filename):

	stds = AsnGlobals.sourceDir
	
	src = os.path.join (stds, filename)
	
	asn = StdDocumentHtml (src)
	dst = os.path.join ("browser", os.path.splitext(filename)[0]+".html")
	print dst
	
	asn.write (dst)
	
def nodeToHtml (asn):
	idNum = "S10274B6"
	id = makeFullId (idNum)
	std = asn[id]
	print std.toHtml()

def tester ():
	"""
	make an html document using only a spefied tree of the standards hierarchy
	"""
	stds = AsnGlobals.sourceDir
	
	path = os.path.join (std, "1996-New-York-Science-localized.xml")

	# Earth Science standards
	asn = StdDocumentHtml (path,"S102A818")

	# All standards
	## asn = StdDocumentHtml (path)

	outPath = "html/asn2.html"
	asn.write (outPath)
	
def makeDirStandardsHtml ():

	stds = AsnGlobals.sourceDir
	dest = "html"
	if not os.path.exists (dest):
		os.mkdir (dest)
	for filename in os.listdir (stds):
		if filename == ".svn": continue
		src = os.path.join (stds, filename)
		
		print src
		asn = StdDocumentHtml (src)
		dst = os.path.join (dest, os.path.splitext(filename)[0]+".html")
		print dst
		
		asn.write (dst)
	
def makeBrowserStdHtml (filename):

	stds = AsnGlobals.sourceDir
	
	src = os.path.join (stds, filename)
	
	asn = StdDocumentHtml (src)
	dst = os.path.join ("/Library/Webserver/Documents/asn-globe", os.path.splitext(filename)[0]+".html")
	print dst
	
	# asn.write (dst)
		
if __name__ == "__main__":
	basedir = "/home/ostwald/Documents/ASN/ASN-2010-0903/Math"
	filename = 'Math-2010-CCSS-Common Core Math'
	path = os.path.join (basedir, filename+'.xml')
	doc = StdDocumentHtml (path)
	## print doc.html
	doc.write ("html/" + filename+'.html')
