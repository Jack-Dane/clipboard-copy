
import pyperclip, time
from threading import Thread
from .Logger import Logger


class ClipboardPoller(Thread, Logger):

    def __init__(self, clipboardQueue):
        super(ClipboardPoller, self).__init__()
        self.setupLogging("Logs/main.log")
        self.clipboardQueue = clipboardQueue
        self.clipboardStack = []
        self.currentClipboardItem = ""
        self.ignoreNext = False

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
        while True:
            currentClipboardItem = pyperclip.paste()
            if currentClipboardItem != self.currentClipboardItem and not self.ignoreNext:
                self.clipboardChange(currentClipboardItem)
            self.ignoreNext = False
            time.sleep(timeSeconds)

    def clipboardChange(self, item=None):
        """
        Change the current item and add the new item to the begining of the list
        :param item: Copied item, could be none and will grab the newest item
        """
        item = item or pyperclip.paste()
        self.clipboardQueue.put(item)
        self.currentClipboardItem = item
        self.clipboardStack.insert(0, item)
        self.loggingChange(self.currentClipboardItem)

    def newClipboardValue(self, clipboardValue):
        """
        Change the current clipboard without effecting Clipboard Data
        :param clipboardValue: New clipboard value
        """
        self.ignoreNext = True
        pyperclip.copy(clipboardValue)

    def getData(self):
        return self.clipboardStack
