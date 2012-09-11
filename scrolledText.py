# a simple text or file viewer component
# Modified slightly from "programming Python", 2d edition
# Biggest modification is gridding instead of packing, after example 24-10
# in Brent Welch's "Practical Programming in Tcl and Tk"

try:
    from tkinter import *
except ImportError:
    from Tkinter import *
import os.path

class ScrolledText(Frame):
    def __init__(self, parent=None, text='', file=None, **kwargs):
        Frame.__init__(self, parent)
        self.makewidgets(**kwargs)
        self.grid(sticky = 'news')
        self.rowconfigure(0, weight = 1)
        self.columnconfigure(0, weight = 1)
        self.settext(text, file)
        self.text.edit_separator()

    def makewidgets(self, **kwargs):
        text = Text(self, relief=SUNKEN, **kwargs)
        self.text = text
        yscroll = Scrollbar(self, orient = VERTICAL)
        xscroll = Scrollbar(self, orient = HORIZONTAL)
        yscroll.config(command=text.yview)
        xscroll.config(command=text.xview)
        text.config(yscrollcommand=yscroll.set)
        text.config(xscrollcommand=xscroll.set)
        text.grid(column = 0, row = 0, sticky = "news")
        yscroll.grid(column = 1, row = 0, sticky= "news")
        xscroll.grid(column = 0, row = 1, sticky = "ew")


    def settext(self, text='', file=None):
        try:
            if file and os.path.exists(file):
                text = open(file, 'r').read()
        except IOError:
            text = 'Failed to open '+ file
        self.text.delete('1.0', END)                     # delete current text
        self.text.insert('1.0', text)                    # add at line 1, col 0
        self.text.mark_set(INSERT, END)                  # set insert cursor
        self.text.see(END)
        self.text.focus()                                # save user a click

    def gettext(self, first='1.0', last = END+'-1c'):    # returns a string
        return self.text.get(first, last)                # first through last

    def clear(self):
        self.text.delete('1.0', END)

    def append(self, text):
        self.text.insert(END, text)
        self.text.see(END)

    def insert(self, text):
        self.text.insert(INSERT, text)
        self.text.see(INSERT)

    # ScrolledText is a proxy for the enclosed Text widget
    def __getattr__(self, name):
        if 'text' not in self.__dict__:
            raise AttributeError
        return getattr(self.text, name)

    # __getattr__ deosn't seem to work for configure, cget

    def configure(self, **kwargs):
        self.text.configure(**kwargs)

    def cget(self, **kwargs):
        self.text.cget(**kwargs)

if __name__ == '__main__':
    root = Tk()
    try:
        st = ScrolledText(file=sys.argv[1], wrap = "none") # filename on cmdline
    except IndexError:
        st = ScrolledText(text='Words\ngo here', wrap = "none")   # or not: 2 lines
    def show(event):
        print (repr(st.gettext()))        # show as raw string
    root.bind('<Key-Escape>', show)       # esc = dump text
    root.mainloop()


