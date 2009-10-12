# This file contains classes that can export lists into various formats.

import tempfile, re

# A class to store information about sentences
# E.g The sentence itself, media information etc

class Sentence:
	def __init__(self, sentence="", media=[], language=""):
		# Initiate variables
		self.sentence = sentence # Blank sentence to begin with.
		self.media = media # A list of media associated with this sentence.
		self.language = language # The language this sentence is in.


# BASE EXPORTER CLASS --------------------------------------------------
class ListExporter:
	# INIT -------------------------------------------------------------
	def __init__(self):
		# VARS
		self.sentences = [] # A list of the sentences to export.
	
	# OPEN TEMP FILE
	def openTempFile(self):
		# Make a temporary file, we need to make sure it doesn't get
		# When we close it.
		file = tempfile.NamedTemporaryFile(delete=False)
		
		# Now return this.
		return file
	
	# READ LIST --------------------------------------------------------
	# This function takes a django List object and extracts the
	# Sentences from it.
	def readList(self, list):
		# Loop through the sentences in the list
		for sentence in list.sentence.all():
			# Now add the sentence to our list
			self.sentences.append(Sentence(sentence=sentence.sentence, media=sentence.media, language=sentence.language))
		
		# Let's read the name of the list for convenience later on.
		self.name = list.name
		
		# Done for now.
			
	
	# EXPORT -----------------------------------------------------------
	# Export the sentences to a file and return the path, so that we can
	# redirect the user to the file. (The file can be outside of the
	# the websites path, as long as the webserver has permission to read
	# the files. We can send a special header in the http request to
	# make the webserver send the file.
	def export(self):
		pass
	
	
# AS TEXT FILE
# This class exports setences into a text file, line seperated.
class TextFileListExporter(ListExporter):
	def export(self):
		# Check if we have any sentences before doing anything.
		if self.sentences:
			
			# Right now open a temporary file and write our sentences to
			# it.
			file = self.openTempFile()
			
			for sentence in self.sentences:
				file.write(sentence.sentence + "\n")
			
			# Before we exit, it would be convenient for use to make a
			# name to use for this file. (even though we can't choose
			# the name of the temporary file)
			self.filename = self.name + ".txt"
			
			# Make sure we strip any spaces
			self.filename = re.sub('\s', '', self.filename)
			
			print self.filename
			
			# We should have a file now, return the file name
			return file.name
		
		# No sentences, fail.
		else:
			return False