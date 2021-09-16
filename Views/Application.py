
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
        self.master.configure(background="#2b2b2b")
        self.master.title("Clipboard")

        self.controller = controller
        self.clipboardStack = clipboardStack

        self.configureStyles()
        self.pack()

        self.configureTreeWidget()
        self.configureButtons()

    def configureStyles(self):
        """
        Configure style to be used
        """
        self.style = ttk.Style()
        self.style.configure("DarkTheme.TButton", foreground="#e3e3e3", background="#2b2b2b")
        self.style.configure("DarkTheme.TFrame", foreground="#e3e3e3", background="#2b2b2b")

    def configureButtons(self):
        """
        Create and configure buttons: confirm & cancel
        """

        # button button frame
        self.buttonFrame = ttk.Frame(self.master, style="DarkTheme.TFrame")
        self.buttonFrame.pack(padx=5, pady=5)

        # confirm button
        self.confirmButton = ttk.Button(self.buttonFrame, command=self.confirmClick, text="Confirm",
                                        style="DarkTheme.TButton")
        self.confirmButton.grid(row=0, column=0, padx=5)

        # cancel button
        self.cancelButton = ttk.Button(self.buttonFrame, command=self.cancelClick, text="Cancel",
                                       style="DarkTheme.TButton")
        self.cancelButton.grid(row=0, column=1, padx=5)

    def configureTreeWidget(self):
        """
        Create the TreeWidget which stores all the clipboard values
        """
        treeViewColumns = ("#1",)
        self.treeView = ttk.Treeview(self.master, columns=treeViewColumns, show="headings", 
                                     takefocus=False)
        self.treeView.heading("#1", text="Clipboard Text")

        for clipboard in self.clipboardStack:
            self.treeView.insert("", tk.END, values=(clipboard,))

        self.treeView.pack(padx=5, pady=5)

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
