
from threading import Thread

import logging
import os
import pyperclip
import time


class ClipboardPoller(Thread):

    def __init__(self, clipboardQueue):
        super(ClipboardPoller, self).__init__()
        self.clipboardQueue = clipboardQueue
        self.clipboardStack = []
        self.currentClipboardItem = ""
        self.ignoreNext = False
        self.maxLength = 30
        self.createCheckLoggingFile("Logs/main.log")

    def run(self):
        """
        Set variables as what is in the current clipboard
        """
        super(ClipboardPoller, self).run()
        currentClipboardItem = pyperclip.paste()
        self.clipboardChange(currentClipboardItem)
        self.checkItemLoop()

    def checkItemLoop(self, timeSeconds=1):
        """
        Initialise loop to see if item has changed
        """
        while True:
            self._checkItem()
            time.sleep(timeSeconds)

    def _checkItem(self):
        """
        Check to see if clipboard has changed
        """
        currentClipboardItem = pyperclip.paste()
        if currentClipboardItem != self.currentClipboardItem and not self.ignoreNext:
            self.clipboardChange(currentClipboardItem)
        self.ignoreNext = False

    def clipboardChange(self, item=None):
        """
        Change the current item and add the new item to the beginning of the list
        :param item: Copied item, could be none and will grab the newest item
        """
        item = item or pyperclip.paste()
        self.clipboardQueue.put(item)
        self.currentClipboardItem = item
        self.addItemToStack(item)
        logging.info(f"Clipboard Change {item}")

    def addItemToStack(self, item):
        """
        Add item to the stack and keep track of total length
        :param item: Copied item to add to the stack
        """
        self.clipboardStack.insert(0, item)
        if len(self.clipboardStack) >= self.maxLength:
            self.clipboardStack = self.clipboardStack[:self.maxLength]

    def createCheckLoggingFile(self, fileLocation):
        """
        Create the logging directory if it has been deleted
        :param fileLocation: the file location of the log file
        """
        os.makedirs(os.path.dirname(fileLocation), exist_ok=True)
        logging.basicConfig(filename=fileLocation, level=logging.INFO)


    def newClipboardValue(self, clipboardValue):
        """
        Change the current clipboard without effecting Clipboard Data
        :param clipboardValue: New clipboard value
        """
        self.ignoreNext = True
        pyperclip.copy(clipboardValue)

    def getData(self):
        return self.clipboardStack
