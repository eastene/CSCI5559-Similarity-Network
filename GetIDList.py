import DBConnection

class getList:
	def __init__(self):
        	self.conn1 = DBConnection.DBConnection()
	
	def GetId(self):
		self.conn1.getSortedPatientIDList()
t = getList()
t.GetId()
