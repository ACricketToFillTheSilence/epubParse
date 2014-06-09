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
	hausa = "ORIGINAL PROVERB"
	translation = "TRANSLATION"
	gen_eng = "GENERAL ENGLISH"
	ig_first = "INITIAL FIRST WORD"
	save_state = ignore
	sentence_count = 0
	curr_proverb_number = 0
	tens_place = 0

	#debugging
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
   			self.sentence_count = 0 	#Each new p signals a new type of entry, this will start the count
   			if self.save_state == self.ignore:
   				self.save_state = self.ig_first
   			if self.save_state != self.hausa:
   				self.save_state = self.first_word


	def handle_charref(self, name):
		if self.isInt(name):
			file_to_write.write(self.unescape("&#"+name+";").encode("utf8"))
		else:
			file_to_write.write(self.unescape("&"+name+";").encode("utf8"))


	def handle_data(self, data):
		global file_to_write
		final_punct = ['.', '!', '?']
		self.prev_data = data
		if data in final_punct and self.save_state != self.ignore:
			if self.save_state == self.hausa:
				self.save_state = self.translation
			elif self.save_state == self.translation:
				self.sentence_count += 1
				if self.sentence_count >2:
					file_to_write.write("\n***SOMETHING LOOKS FISHY***\n")

		elif self.save_state == self.first_word:
			if self.isInt(data):
				self.save_state = self.hausa
				data = "#"+data
				self.curr_proverb_number+=1
				if self.curr_proverb_number == 9:
					self.tens_place += 10
			else:
				self.save_state = self.gen_eng

		elif self.save_state == self.ig_first:
			if self.isInt(data):
				self.save_state = self.hausa
			else:
				self.save_state = self.ignore

		if self.save_state != self.ignore:
			file_to_write.write(data)

		

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
