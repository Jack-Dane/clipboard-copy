
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

        # confirm button
        self.confirmButton = ttk.Button(self.master, command=self.confirmClick, text="Confirm")
        self.confirmButton.pack()

        # cancel button
        self.cancelButton = ttk.Button(self.master, command=self.cancelClick, text="Cancel")
        self.cancelButton.pack()

    def configureTreeWidget(self):
        """
        Create the TreeWidget which stores all the clipboard values
        """
        self.treeView.heading("#1", text="Clipboard Text")

        for clipboard in self.clipboardStack:
            self.treeView.insert("", tk.END, values=(clipboard,))

        self.treeView.pack()

    def confirmClick(self):
        """
        Create the Copy and Close Buttons
        """
        selectionValue = self.treeView.item(self.treeView.selection()[0])["values"][0]
        self.controller.copyClipboard(selectionValue)
        self.master.destroy()
        

    def cancelClick(self):
        """
        Close the window
        """
        self.master.destroy()
