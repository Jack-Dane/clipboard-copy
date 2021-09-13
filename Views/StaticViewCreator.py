
from . import Application

class StaticViewCreator:

	@staticmethod
	def initialiseView():
		root = tk.Tk()
		view = Application(self.clipboardData.clipboardStack, self, master=root)
		view.mainloop()
