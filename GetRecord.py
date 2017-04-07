import DBConnection

class getRecord:
	def __init__(self):
        	self.conn1 = DBConnection.DBConnection()
	
	def Getdata(self):
		self.conn1.getPatient("TCGA-A2-A0CL-01A-11R-A115-07")
t = getRecord()
t.Getdata()
