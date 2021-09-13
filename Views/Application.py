
import tkinter as tk
from tkinter import ttk


class Application(tk.Frame):

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
        self.controller.copyClipboard()
        for clipboardItem in self.treeView.selection():
            pyperclip.copy(self.treeView.item(clipboardItem)["values"][0])

