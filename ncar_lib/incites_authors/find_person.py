"""
get candidates - given a fullname, do a search and return results

strategy:
	first search by first and last name, if there are collisions, try to resolve with
	middle name ...
	
HOW does peopleDB handle the following names with more than 2 "other names"
WARNING: "Brown, W. O. J." has more than 2 other names
WARNING: "Brown, William J. O." has more than 2 other names
WARNING: "Brown, William O. J." has more than 2 other names
--> middleName = O J
WARNING: "Moore, D. J. P." has more than 2 other names
WARNING: "Moore, David J. P." has more than 2 other names
--> No middle name!
WARNING: "Rizvi, S. R. H." has more than 2 other names
--> middleName: Rafat Husain
WARNING: "Wigley, T. M. L." has more than 2 other names
WARNING: "Wigley, Tom M. L." has more than 2 other names
--> middleName: M L
"""
import sys, os
from ncar_lib.peopledb import PersonSearcher, Person, NameUtils

def resolveFullName (fullname):
	"""
	returns (first, middle, last, note
	"""
	first = middle = last = notes = ''
	
	def strip_trailing_dot (x):
		if x is None or len(x) == 0:
			return x
		elif x[-1] == '.':
			return x[:-1]
		else:
			return x
	
	comma_splits = map (lambda x:x.strip(), fullname.split(','))
	last = comma_splits[0]
	initial_splits = map (lambda x:x.strip(),comma_splits[1].split(' '))
	note = ""
	if len(initial_splits) > 2:
		# raise Exception, "more than 2 other names"
		note = 'WARNING: "%s" has more than 2 other names' % fullname
	middle = len(initial_splits) > 1 and initial_splits[1] or ''
	first = initial_splits[0]
	return strip_trailing_dot(first), strip_trailing_dot(middle), last, note

class PersonFinder (NameUtils):
	"""
	finds people in peopleDB best matching "fullname"
	
	1 - seach peopleDB for lastName, exact match
	2 - eliminate by first initial (careful for hyphens)
	"""
	verbose = 0
	
	def __init__ (self, fullname):
		self.fullname = fullname
		self.firstName, self.middleName, self.lastName, self.note = resolveFullName (fullname)
		params = { 
			'exactNameMatch' : 'true',
			# 'firstName' : self.firstName,
			'lastName' : self.lastName
		}
		self.searcher = PersonSearcher(params)
		candidates = map (Person, self.searcher.data)
		
		# first filter: first initial
		if self.firstName:
			candidates = self.filterByFirstInitial(candidates)
			if self.verbose:
				print "%d after filterByFirstInitial" % len(candidates)
			
			# second filter: first name
			if self.firstName and len(self.firstName) > 1:
				candidates = self.filterByFirstName(candidates)
				if self.verbose:
					print "%d after filterByFirstName" % len(candidates)
		
		# middle filter: middle initial
		if self.middleName:
			candidates = self.filterByMiddleInitial(candidates)
			
			# second filter: middle name
			if len(self.middleName) > 1:
				candidates = self.filterByMiddleName(candidates)
			
		self.candidates = candidates
			
		if self.verbose:
			print "%d candidates found for %s (%s | %s)" % (len(self.candidates), self.fullname, self.lastName, self.firstName)
			
	def filterByFirstInitial (self, candidates):
		"""
		filter those results that have a DIFFERENT first initial. we can only eliminate when self has a first
		initial AND other has first initial and these do NOT match.
		- if self has no initial, filter none
		- if candidate has no initial, do not filter it
		"""
		# print "%d candidates" % len(candidates)
		if not self.firstName:
			return candidates
		filtered=[];add=filtered.append
		myFirstInitial = self.getFirstInitial()
		for i, person in enumerate(candidates):
			# print '%d : %s' % (i, person)
			initial = person.getFirstInitial()
			if not initial:
				add(person)
				continue
			if initial == myFirstInitial:
				add(person)
		return filtered
			
	def filterByFirstName (self, candidates):
		"""
		filter those results that have a DIFFERENT first name. we can only eliminate when 
		BOTH have a first name and the names don't match
		- if self has no initial, filter none
		- if candidate has no initial, do not filter it
		"""
		# print "%d candidates" % len(candidates)
		if not self.firstName or len(self.firstName) < 2:
			return candidates
		filtered=[];add=filtered.append
		for i, person in enumerate(candidates):
			## print '%d : %s' % (i, person)
			if not person.firstName or len(person.firstName) <2:
				add(person)
				continue
			if person.firstName == self.firstName:
				add(person)
		return filtered
			
	def filterByMiddleInitial (self, candidates):
		"""
		filter those results that have a DIFFERENT middle initial. we can only eliminate when self has a 
		initial AND other has  initial and these do NOT match.
		- if self has no initial, filter none
		- if candidate has no initial, do not filter it
		"""
		# print "%d candidates" % len(candidates)
		if not self.middleName:
			return candidates
		filtered=[];add=filtered.append
		myMiddleInitial = self.getMiddleInitial()
		for i, person in enumerate(candidates):
			# print '%d : %s' % (i, person)
			initial = person.getMiddleInitial()
			if not initial:
				add(person)
				continue
			if initial == myMiddleInitial:
				add(person)
		return filtered
		
	def filterByMiddleName (self, candidates):
		"""
		filter those results that have a DIFFERENT middle name. we can only eliminate when 
		BOTH have a middle name and the names don't match
		- if self has no initial, filter none
		- if candidate has no initial, do not filter it
		"""
		# print "%d candidates" % len(candidates)
		if not self.middleName or len(self.middleName) < 2:
			return candidates
		filtered=[];add=filtered.append
		for i, person in enumerate(candidates):
			# print '%d : %s' % (i, person)
			if not person.middleName or len(person.middleName) < 2:
				add(person)
				continue
			if person.middleName == self.middleName:
				add(person)
		return filtered
		
	def reportCandidates (self):
		print "%d candidates found for %s (%s | %s)" % (len(self.candidates), self.fullname, self.lastName, self.firstName)
		for person in self.candidates:
			print person
		
if __name__ == '__main__':
	
	name = 'Anderson, Jeff'
	if len(sys.argv) > 1:
		name = sys.argv[1]
	finder = PersonFinder (name)
	finder.reportCandidates()
