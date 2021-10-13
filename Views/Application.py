
import tkinter as tk
from tkinter import ttk


class StaticViewCreator():

    @staticmethod
    def initialiseView(model, clipboardQueue):
        """
        Intialises the Application View
        :param clipboardStack: a list of clipboard items
        :param controller: the controller which is calling the view
        """
        root = tk.Tk()
        view = Application(model, clipboardQueue, master=root)
        view.mainloop()


class Application(tk.Frame, StaticViewCreator):

    def __init__(self, model, clipboardQueue, master=None):
        super().__init__(master)
        self.master = master
        self.master.configure(background="#2b2b2b")
        self.master.title("Clipboard")
        self.master.resizable(width=False, height=False)
        self.master.iconphoto(False, tk.PhotoImage(file="Assets/icon.png"))
        
        self.model = model
        self.clipboardStack = self.model.getData()

        self.configureStyles()
        self.pack()

        self.configureTreeWidget()
        self.configureButtons()

        self.clipboardQueue = clipboardQueue
        self.master.after(100, self.checkForUpdated)

    def configureStyles(self):
        """
        Configure style to be used
        """
        self.style = ttk.Style()
        self.style.configure("DarkTheme.TButton", foreground="#e3e3e3", background="#2b2b2b")
        self.style.map("DarkTheme.TButton", background=[("active", "#007804")])
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
                                     takefocus=False, style="DarkTheme.Treeview")
        self.treeView.heading("#1", text="Clipboard Text")
        self.attachTreeWidget()

        self.treeView.pack(padx=5, pady=5)

    def attachTreeWidget(self):
        """
        Attach the tree widget to the clipboard list in the model
        """
        self.clipboardStack = self.model.clipboardStack
        for clipboard in self.model.getData():
            self.treeView.insert("", tk.END, values=(clipboard,))

    def confirmClick(self):
        """
        Create the Copy and Close Buttons
        """
        selectionValue = self.treeView.item(self.treeView.selection()[0])["values"][0]
        self.model.newClipboardValue(selectionValue)
        self.master.destroy()

    def cancelClick(self):
        """
        Close the window
        """
        self.master.destroy()

    def clearTreeWidget(self):
        """
        Remove all the items from the treeWidget
        """
        for item in self.treeView.get_children():
            self.treeView.delete(item)

    def addAnotherClipboard(self, copyItem):
        """
        Add another clipboard item to the application while live running
        """
        self.treeView.insert("", tk.END, values=(copyItem, ))

    def checkForUpdated(self):
        """
        If new item has been added to the clipboard queue, update the list items
        """
        if not self.clipboardQueue.empty():
            self.update()
            self.clipboardQueue.clear()

        self.master.after(100, self.checkForUpdated)

    def update(self):
        """
        Called when the model is updated, instead of updating incase of other CRUD methods
        """
        self.clearTreeWidget()
        self.attachTreeWidget()
