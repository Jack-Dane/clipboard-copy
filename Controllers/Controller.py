
from threading import Thread
import keyboard


class Controller(Thread):

    def __init__(self, inputWait="ctrl+alt+v"):
        super(Controller, self).__init__()
        self.inputWait = inputWait
        self.clipboardData = None
        self.view = None

    def run(self):
        super(Controller, self).run()
        self.waitForInput()

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

    def waitForInput(self):
        """
        Wait till the keyboard input matches watched specified
        When it does, intialise the view attached
        """
        keyboard.wait(self.inputWait)
        self.initialiseView()
        self.waitForInput()

    def initialiseView(self):
        """
        Open the TKinter window which will show the
        """
        self.view.initialiseView(self.clipboardData.clipboardStack, self)

    def copyClipboard(self, clipboardText):
        """
        Copy the selected text into the users clipboard
        """
        self.clipboardData.newClipboardValue(clipboardText)
