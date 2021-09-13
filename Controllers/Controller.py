
from threading import Thread
import keyboard


class Controller(Thread):

    def __init__(self):
        super(Controller, self).__init__()
        self.clipboardData = None
        self.view = None

    def attachModel(self, clipboardData):
        """
        Attach the backend to the front end
        :param clipboardData: clipboardPoller Class
        """
        self.clipboardData = clipboardData


    def attachView(self, view):
        """
        Attach the view to the controller
        :param view: the static view intiliser
        """
        self.view = view


    def run(self):
        super(Controller, self).run()
        self.waitForInput()

    def waitForInput(self):
        keyboard.wait("ctrl+shift+v")
        self.initialiseView()
        self.waitForInput()

    def initialiseView(self):
        """
        Open the TKinter window which will show the
        """
        self.view.initialiseView()

    def copyClipboard(self, clipboardText):
        pass
