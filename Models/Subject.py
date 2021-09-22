
class Subject:

	def __init__(self):
		self.observers = []

	def addObserver(self, observer):
		"""
		Add observer to list of observers
		"""
		self.observers.append(observer)

	def removeObserver(self, observer):
		"""
		Remove observer from list of observers
		"""
		self.observers.remove(observer)

	def notifyObservers(self):
		"""
		Notify observers when a change has occured
		"""
		for observer in self.observers:
			observer.update()
