import DBConnection

class Updatetest:
	def __init__(self):
    		self.conn1 = DBConnection.DBConnection()
	
	def AttrUpdate(self):
		self.conn1.updateAttribute("TCGA-A2-A0CV-01A-31R-A115-07","G30",1.50)
t = Updatetest()
t.AttrUpdate()
