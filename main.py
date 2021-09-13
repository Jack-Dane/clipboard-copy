import pyperclip, time, logging, tkinter, keyboard
from threading import Thread
from tkinter import ttk


class Logger:

    def setupLogging(self, filepath):
        """
        Setup the logging file
        :param filepath: filepath of log file
        """
        logging.basicConfig(filename=filepath, level=logging.INFO)

    def loggingChange(self, change):
        """
        Log changes in file
        :param change: item that needs to be logged
        """
        logging.info(f"Clipboard Change {change}")


class ClipboardPoller(Thread, Logger):

    def __init__(self):
        super(ClipboardPoller, self).__init__()
        self.setupLogging("main.log")
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
        root = tkinter.Tk()
        view = Application(self.clipboardData.clipboardStack, self, master=root)
        view.mainloop()

    def copyClipboard(self, clipboardText):
        pass


class Application(tkinter.Frame):

    def __init__(self, clipboardStack, controller, master=None):
        super().__init__(master)
        self.master = master
        self.controller = controller
        self.clipboardStack = clipboardStack
        self.pack()

        treeViewColumns = ("#1",)
        self.treeView = ttk.Treeview(self.master, columns=treeViewColumns, show="headings", takefocus=False)

        self.configureTreeWidget()

    def configureTreeWidget(self):
        """
        Create the TreeWidget which stores all the clipboard values
        """
        self.treeView.heading("#1", text="Clipboard Text")

        for clipboard in self.clipboardStack:
            self.treeView.insert("", tkinter.END, values=(clipboard,))

        self.treeView.bind('<<TreeviewSelect>>', self.clipboardClick)
        self.treeView.pack()

    def clipboardClick(self, event):
        """
        When item is selected in list the value copied to the clipboard
        """
        self.controller.copyClipboard()
        for clipboardItem in self.treeView.selection():
            pyperclip.copy(self.treeView.item(clipboardItem)["values"][0])


def main():
    clipboardPoller = ClipboardPoller()
    clipboardPoller.start()

    controller = Controller()
    controller.start()
    controller.attachModel(clipboardPoller)


if __name__ == "__main__":
    main()
