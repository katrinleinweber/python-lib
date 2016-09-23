import sys, os
from UserList import UserList
from UserDict import UserDict

txtDir = "H:/python-lib/SAT_Analysis/txtFiles"
txtFile = "Applied_5-8_S101EF6F_done.txt"

path = os.path.join (txtDir, txtFile)

class Schema (UserList):
	def __init__ (self, line):
		self.data = line.split('\t')

	def report (self):
		print "Schema"
		for i in range (len (self.data)):
			print "\t%d: '%s'" % (i, self[i])

class Record:
	def __init__ (self, line, schema):
		self.data = line.split ('\t')
		self.schema = schema

	def __getitem__ (self, field):

		index = self.schema.index (field)
		# print "getItem: %s (%d)" % ( field, index)		
		if (index is not None):
			return self.data[index]

	def __setitem__ (self, field, value):
		try:
			index = self.schema.index (field)
			self.data[index] = value
		except:
			print "tried to find field: " + field
			

class Standard (Record):
	def __init__ (self, data, schema):
		Record.__init__ (self, data, schema)
		self.doc = self['Standards Doc']
		self.id = self['id']
		self.relevance = self['relevant']
		self.text = self['text']
		self.benchmark = self['benchmark']
		self.rank = None
		
	def setDoc (self, doc):
		self.doc = doc

	def setRank (self, rank):
		self.rank = rank

	def isStateStandard (self):
		return self.doc != "NSES"

class NSESDataSet (UserDict):
	"""
	stores standards sets keyed by "standards_doc", e.g. NSES, Colorado, etc
	"""

	def __init__ (self, path):
		UserDict.__init__ (self, {})
		self.path = path
		s = open (path,"r").read()
		

		lines = s.split ('\n')
		print "%d lines read" % len (lines)

		self.schema = Schema (lines[0])
		# self.schema.report()
		
		current_set = None
		rank_counter = 1
		for line in lines[1:]:
			if not line.strip():
				continue
			rec = Standard (line, self.schema)
			print "doc: %s id: %s" % (rec.doc, rec.id)
			if not rec.doc:
				rec.setDoc (current_set)
				rank_counter = rank_counter + 1
			else:
				current_set = rec.doc
				rank_counter = 1
			if rec.isStateStandard():
				rec.setRank (rank_counter)
			self._add_rec (rec)


	def _add_rec (self, rec):
		set = rec.doc
		if not self.has_key(set):
			self[set] = []
		items = self[set]
		items.append (rec)
		self[set] = items
		

	def _make_rec (self, line):
		return Standard (line, self.schema)


if __name__ == "__main__":
	r = NSESDataSet (path)

	print "schema"
	for field in r.schema:
		print "\t" + field
		
	for set in r.keys():
		if set == "NSES": continue
		print "\n** %s **" % set
		for s in r[set]:
			print "\t%s (%d) -> %s" % (s.id, s.rank, s.relevance)
	
