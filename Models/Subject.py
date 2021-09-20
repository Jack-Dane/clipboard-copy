
class Subject:

	def __init__(self):
		self.observers = []

	def addObserver(self, observer):
		self.observers.append(observer)

	def removeObserver(self, observer):
		self.observers.remove(observer)

	def notifyObservers(self):
		for observer in self.observers:
			observer.update()
