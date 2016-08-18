import sys

class LineReader:

	def __init__(self):
		self.fname = ""
		
	def init_from_sys(self):
		if (len(sys.argv) < 2) :
			raise ValueError( sys.argv.pop() + "[filename]")			
		self.fname = sys.argv.pop()
	
	def set_file_name(self, fname):
		self.fname = fname
				
	def simple_line_read(self):
		with open(self.fname) as fp:
			for line in fp:        
				self.do(line)

	#Abstract method which performs action
	def do(self, line):
		raise NotImplementedError("do() is not implemented in this instance")