from HTMLParser import HTMLParser
import htmlentitydefs
import os #, subprocess

import sys, getopt

import re

 
#currString = ''
file_to_write = open('/Applications/djangostack-1.5.8-0/apps/django/django_projects/Project/tester.rtf', 'w')

class EpubHTMLParser(HTMLParser):
	ignore = "DON'T SAVE"
	first_word = "FIRST WORD AFTER INITIAL TAG"
	main_body_first = "IN THE MAIN BODY OF THE TEXT"
	hausa = "ORIGINAL PROVERB"
	english = "TRANSLATION"
	save_state = ignore

	prev_data = ""

	def isInt(self, letters):
		try:
			return type(int(letters)) == int
		except ValueError:
			return False

	#the following function was written by Frederik Lundh and published on January 15, 2003
	def unescape(self, text):
		def fixup(m):
			text = m.group(0)
			if text[:2] == "&#":
            	# character reference
				try:
					if text[:3] == "&#x":
						return unichr(int(text[3:-1], 16))
					else:
						return unichr(int(text[2:-1]))
				except ValueError:
					pass
			else:
            	# named entity
				try:
					text = unichr(htmlentitydefs.name2codepoint[text[1:-1]])
				except KeyError:
					pass
			return text # leave as is
		return re.sub("&#?\w+;", fixup, text)
	#End borrowed code

	def handle_starttag(self, tag, attrs):
		global file_to_write
   		if tag == 'p':
   			if self.save_state ==self.english:
   				self.save_state = self.main_body_first
   			else:
				self.save_state = self.first_word
				#print "Encountered a start tag:", tag, "with attributes", attrs

	def handle_charref(self, name):
		if self.isInt(name):
			print "name: ", name
			file_to_write.write(self.unescape("&#"+name+";").encode("utf8"))
		else:
			file_to_write.write(self.unescape("&"+name+";").encode("utf8"))


	def handle_endtag(self, tag):
		#global file_to_write
		if tag == 'p':
			if self.save_state == self.hausa:
				self.save_state = self.first_word
			elif self.save_state == self.english:
				self.save_state = self.main_body_first
			else:
				self.save_state = self.ignore
			#print "Encountered an end tag :", tag

	def handle_data(self, data):
		global file_to_write
		final_punct = ['.', '!', '?']
		#if data == '\n':
			#print "It does see new lines!"
			#print "save state"+self.save_state
			#print "What was there before: ", self.prev_data
			#file_to_write.write("**HERE'S THE NEWLINE**")
		self.prev_data = data
		if self.save_state == self.first_word:
			if self.isInt(data):
				file_to_write.write("#"+data)
				self.save_state = self.hausa
			else:
				self.save_state = self.ignore

		elif self.save_state == self.main_body_first:
			if self.isInt(data):
				file_to_write.write("#"+data)
				self.save_state = self.hausa
			else:
				file_to_write.write(data)
				self.save_state = self.english

		elif self.save_state == self.hausa:
			if data in final_punct:
				file_to_write.write(data+'\n')
				self.save_state = self.english
			else:
				file_to_write.write(data)

		elif self.save_state == self.english:
			if data in final_punct:
				file_to_write.write(data+'\n')
				#self.save_state = self.english
			else:
				file_to_write.write(data)
		# 	if self.isInt(data):
		# 		#print "The string is interpreted as an int: ", data
		# 		file_to_write.write("#"+data)
		# 		self.save_state = self.hausa
		# 	else:
		# 		file_to_write.write(data)
		# 		self.save_state = hausa
		# elif self.save_state == self.main_body_first:
		# 	if self.isInt(data):
		# 		file_to_write.write("#"+data)
		# 		self.save_state = self.hausa
		# 	else:
		# 		file_to_write.write(data)
		# 		self.save_state = self.english
		# else:
		# 	self.save_state = self.ignore

		# elif self.save_state == self.hausa:
		# 	file_to_write.write(data)
		# 	if data in final_punct:
		# 		file_to_write.write('\n')
		# 		self.save_state = self.english
		
		# elif self.save_state == self.english:
		# 	file_to_write.write(data)
		# 	if data in final_punct:
		# 		file_to_write.write('\n')

		#file_to_write.write(unichr(currString).encode('utf-8'))

		# if self.save_state == self.first_word:
		# 	print "First Word: ", data
		# 	currString += ' '+str(data)
		# 	self.save_state = self.save
		# elif self.save_state == self.save:
		# 	print "Gen word: ", data
		# 	currString += str(data)
		# elif self.save_state == self.inside_tag:
		# 	print "just inside the tag", data
		# 	if type(data[0]) is int and type(data[-1]) is str:
		# 		self.save_state = self.preceding_sentence
		# elif self.save_state == self.preceding_sentence:
		# 	print "Hausa sentence: ", data
		# 	if data[-1] == '.':
		# 		self.save_state = first_word


#Based off the assumption that 1. the proverbs are in a numbered list format, and 2. Each entry is separated by a paragraph
def epubParse(the_file):
	parser = EpubHTMLParser()#encoding = 'utf-8')

	with open(the_file) as epubFile:
		c = epubFile.read(1)
		while(c):
			parser.feed(c)
			c = epubFile.read(1)

def print_to_file(folder, output_file_name):
	global file_to_write
	try:
		file_to_write = open(folder+output_file_name, 'w')
		for doc in os.listdir(folder):
			epubParse(folder+doc)
			print "Successfully processed document: " + doc
	except OSError:
		print "Problems arose in the print to file function. Change your directory."

def reprocess_file(folder, output_file_name):
	with open(folder+output_file_name, 'r') as output:
		for line in output:
			if line[0] == "#":
				r = 0
				#wait until the next period, then check to see how long the next passage is. If it's ridiculously long (>3),
				#flag it as strange-looking
			continue
		return


############# Command line initialization #############

def main(argv = None):
	try:
		opts, args = getopt.getopt(sys.argv[1:], 'h', ['help'])
	except getopt.error, msg:
		print msg
		print "for help use --help"
		sys.extit(2)

	for o in opts:
		if o in ("-h", "--help"):
			print "The only argument needed is the location of the directory of the html files you'd like to parse."
			sys.exit(0)
	if len(args) == 1:
		print "Yay, you only gave one argument! Now we can process it."
		for arg in args:
			process(arg)
	else:
		print "Please try to limit yourself to one directory and start over."
		sys.exit(0)

def process(arg):
	try:
		print_to_file(arg, 'parsed_data.txt')
	except OSError:
		print "This directory doesn't work: ", arg


#if __name__ == "__main__":
#	main()

path = '/Applications/djangostack-1.5.8-0/apps/django/django_projects/Project/hausa_files/'
#filename = 'content-0009.xml'

print_to_file(path, 'concat_output.txt')
