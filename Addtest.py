import DBConnection

class test:
	def __init__(self):
        	self.conn1 = DBConnection.DBConnection()
	
	def AttrAdd(self):
		self.conn1.addAttributes("TCGA-A2-A0CL-01A-11R-A115-07",{"G300":1.00})
t = test()
t.AttrAdd()
