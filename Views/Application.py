
import tkinter as tk
from tkinter import ttk


class StaticViewCreator:

    @staticmethod
    def initialiseView(clipboardStack, controller):
        """
        Intialises the Application View
        :param clipboardStack: a list of clipboard items
        :param controller: the controller which is calling the view
        """
        root = tk.Tk()
        view = Application(clipboardStack, controller, master=root)
        view.mainloop()


class Application(tk.Frame, StaticViewCreator):

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
            self.treeView.insert("", tk.END, values=(clipboard,))

        self.treeView.bind('<<TreeviewSelect>>', self.clipboardClick)
        self.treeView.pack()

    def clipboardClick(self, event):
        """
        When item is selected in list the value copied to the clipboard
        """
        selectionValue = self.treeView.item(self.treeView.selection()[0])["values"][0]
        self.controller.copyClipboard(selectionValue)
