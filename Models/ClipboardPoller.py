
import pyperclip, time
from threading import Thread
from . import Logger


class ClipboardPoller(Thread, Logger.Logger):

    def __init__(self):
        super(ClipboardPoller, self).__init__()
        self.setupLogging("Logs/main.log")
        self.clipboardStack = []
        self.currentClipboardItem = ""

    def run(self):
        """
        Set variables as what is in the current clipboard
        """
        super(ClipboardPoller, self).run()
        currentClipboardItem = pyperclip.paste()
        self.clipboardChange(currentClipboardItem)
        self.checkItem()

    def checkItem(self, timeSeconds=1):
        """
        Check to see if the clipboard has changed
        """
        currentClipboardItem = pyperclip.paste()
        if currentClipboardItem != self.currentClipboardItem:
            self.clipboardChange(currentClipboardItem)
        time.sleep(timeSeconds)
        self.checkItem()

    def clipboardChange(self, item=None):
        """
        Change the current item and add the new item to the begining of the list
        :param item: Copied item, could be none and will grab the newest item
        """
        item = item or pyperclip.paste()
        self.currentClipboardItem = item
        self.clipboardStack.insert(0, item)
        self.loggingChange(self.currentClipboardItem)

    def newClipboardValue(self, clipboardValue):
        """
        Change the current clipboard without effecting Clipboard Data
        :param clipboardValue: New clipboard value
        """
        pyperclip.copy(clipboardValue)
