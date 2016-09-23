"""


"""
import string
import time
from UserDict import UserDict
from UserList import UserList
from IdmapDB import WebPubDB, BolideDB
from messages import Messages

class MessageMap (UserDict):
	"""
	stores messages for particular collection in particular db as map keyed by id.
	map bickets are lists containing all messages for that id
	"""
	
	def __init__ (self, collKey, db):
		UserDict.__init__(self)
		self.name = db.name
		messages = Messages (db, collKey)
		for msg in messages:
			id = msg['id']
			if not self.has_key (id):
				self[id] = []
			val = self[id]
			val.append (msg)
			self[id] = val
		
class MessageReport:

	"""
	compare messages generated by different DBs for a given collection

	"""

	def __init__ (self, collKey, dbs):
		self.dbs = dbs
		self.collKey = collKey
		self.msgGroups = {}
		for db in dbs:
			msgmap = MessageMap (self.collKey, db)
			self.msgGroups[db.name] = msgmap
		self.ids = self.getIdList ()
		
	def getIdList (self):
		ids = []
		for grp in self.msgGroups.values():
			for id in grp.keys():
				if not id in ids:
					ids.append(id)
		return ids
		
	def report (self):
		print "Message Report for collection: %s" % self.collKey
		print "Databases"
		for grp in self.msgGroups.values():
			print "%s (%d)" %  (grp.name, len (grp))
				
			   
if __name__ == "__main__":
	dbs = [WebPubDB(), BolideDB()]
	collKey = "sercstrtpt"
	rep = MessageReport (collKey, dbs)
	rep.report()
	
