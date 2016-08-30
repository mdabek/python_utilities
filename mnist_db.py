import struct
import numpy as np

class Mnist_DB_File:

	def __init__(self, fname, label=False):
		self.fname = fname;
		self.item_count = 0
	
	def check_magic(self, b_magic):
		magic = struct.unpack('>i', b_magic)[0]
		return magic == self.magic
		
	def process_file(self, fhandle):
		raise NotImpemented("Check magic number not implemented")
	
	def get_items_count(self, b_items):
		self.items_count = struct.unpack('>i', b_items)[0]
		return self.items_count
		
	def load(self):
		f = open(self.fname, "rb")
		try:
			byte_magic = f.read(4)
			byte_items = f.read(4)
			
			if not self.check_magic(byte_magic):
				raise TypeError("Invalid magic number")
			
			self.item_count = self.get_items_count(byte_items)
			self.process_file(f)
		finally:
			f.close()
			
#TRAINING SET IMAGE FILE (train-images-idx3-ubyte):

#[offset] [type]          [value]          [description] 
#0000     32 bit integer  0x00000803(2051) magic number 
#0004     32 bit integer  60000            number of images 
#0008     32 bit integer  28               number of rows 
#0012     32 bit integer  28               number of columns 
#0016     unsigned byte   ??               pixel 
#0017     unsigned byte   ??               pixel 
#........ 
#xxxx     unsigned byte   ??               pixel
class Mnist_DB_Image(Mnist_DB_File):

	magic = 2051
	rows = 0
	cols = 0
	images = []

	def process_file(self, fhandle):
		b_rows = fhandle.read(4)
		b_cols = fhandle.read(4)
		
		self.rows = struct.unpack('>i', b_rows)[0]
		self.cols = struct.unpack('>i', b_cols)[0]
		
		for i in range(self.items_count):
			bd = np.fromfile(fhandle, dtype=np.dtype(np.uint8), count=(self.cols*self.rows))
			self.images.append(bd.reshape(self.cols, self.rows))

		#print("MnistDBImage rows:{0} cols{1}".format(self.rows, self.cols))
	
	def __len__(self):
		return len(self.images)

	def __getitem__(self, key):
		return self.images[key]
			
#TRAINING SET LABEL FILE (train-labels-idx1-ubyte):

#[offset] [type]          [value]          [description] 
#0000     32 bit integer  0x00000801(2049) magic number (MSB first) 
#0004     32 bit integer  60000            number of items 
#0008     unsigned byte   ??               label 
#0009     unsigned byte   ??               label 
#........ 
#xxxx     unsigned byte   ??               label

class Mnist_DB_Label(Mnist_DB_File):

	magic = 2049
	labels = []

	def process_file(self, fhandle):
		bd = fhandle.read(1)
		while bd != b"":
			label = struct.unpack('B', bd)
			self.labels.extend(label)
			bd = fhandle.read(1)
	
	def __len__(self):
		return len(self.labels)

	def __getitem__(self, key):
		return self.labels[key]
	
			
class Mnist_DB:

	def __init__(self, img_fname, label_fname):
		self.images = Mnist_DB_Image(img_fname, False)
		self.labels = Mnist_DB_Label(label_fname, True)
		
	def load_data(self):
		self.images.load()
		self.labels.load()
		
	def images(self):
		return self.images
		
	def labels(self):
		return self.labels