def __init__(self, master, title, val):
    LabelFrame.__init__(self, master, text=title)
    self.hexvar = StringVar()
    self.hexvar.set(val)
    cmd = (self.register(self.validate), "%P")
    entry = Entry(self, textvariable=self.hexvar, validate="key", validatecommand=cmd)
    entry.grid(row=0,column=0,sticky='ew')
    self.columnconfigure(0, weight=1)

def get(self):
    try:
        return bytes.fromhex(self.hexvar.get())
    except ValueError:
        showerror("Invalid Hex String", "You need a whole number of bytes.")
        return None

def validate(self, proposed):
    return all([c in '1234567890abcdefABCDEF ' for c in proposed])
