from __future__ import division         # for python 2
import sys
if sys.version_info[0] == 2:
    from Tkinter import *
    from tkFont import Font
    from tkMessageBox import showinfo
else:
    from tkinter import *
    from tkinter.font import Font
    from tkinter.messagebox import showinfo

from datetime import date, datetime
import random, re, os.path
from stopwatch import StopWatch
from scrolledText import ScrolledText

days = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")
months = ("dummy", "January", "February", "March", "April", "May", "June", "July",
          "August", "September", "October", "November", "December")
monthDays = (0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)

def isLeap(y):
    return (y % 4 == 0) and ( y % 100 != 0 or y % 400 == 0)

class Board(Frame):
    def __init__(self, parent, height = 600, width = 600, bg = 'white'):
        Frame.__init__(self,parent)
        self.parent = parent
        self.grid()

        self.makeMenu()

        try:
            exec(open('weekday.ini').read())
        except IOError:
            self.minyear = -99999
            self.maxyear = 99999
            self.timeout = 0

        self.watch = StopWatch(self, self.timeout)
        self.watch.grid(row=0, column = 2, columnspan = 3, pady = 3)

        self.makeQandA()
        self.makeButtons()
        self.makeLog()
        self.session = SessionStats(self.parent)
        self.session.grid(row = 3, column  = 0, sticky="ew")

        parent.wm_protocol("WM_DELETE_WINDOW", self.onClose)
        self.bind('<Map>', self.map)
        self.bind('<Unmap>', self.unmap)
        self.bind_all('<<TimeLimitExpired>>', self.onTimeExpired)
        random.seed()

    def makeMenu(self):
        top = self.winfo_toplevel()
        menuBar = Menu(top)
        top["menu"] = menuBar

        helpMenu = Menu(menuBar, tearoff=False)
        settingsMenu = Menu(menuBar, tearoff = False)

        menuBar.add_cascade(label="Help", menu = helpMenu)
        helpMenu.add_cascade(label="Algorithm", command=self.helpAlgorithm)
        helpMenu.add_command(label="About", command=self.about)

        menuBar.add_cascade(label="Settings", menu = settingsMenu)
        settingsMenu.add_cascade(label="Year", command=self.getYearSettings)
        settingsMenu.add_command(label="Timeout", command=self.getTimeoutSettings)

    def makeButtons(self):
        buttonBar = Frame(self, relief = SUNKEN, bd = 2)
        buttonBar.grid(row = 3, column = 0, columnspan = 7, pady = 3)
        self.response = IntVar()
        for k in range(7):
            r = Radiobutton(buttonBar, text=days[k][:3].upper(), variable = self.response,
                            value = k+1)
            r.grid(row = 0, column = k, pady = 2, ipady = 1, ipadx = 1)
        self.response.set(1)
        buttonBar = Frame(self, relief = SUNKEN, bd = 2)
        buttonBar.grid(row = 4, column = 1, columnspan = 5, pady = 3, sticky = 'ew')
        self.playButton = Button(buttonBar, text = "Play", command=self.play)
        self.okayButton = Button(buttonBar, text = "Okay", command=self.okay)
        self.setButton = Button(buttonBar, text = "Set", command=self.set)
        self.playButton.grid(pady = 3, column = 0, row = 0, ipadx = 2)
        self.okayButton.grid(pady = 3, column = 1, row = 0, ipadx = 2)
        self.setButton.grid(pady = 3, column = 2, row = 0, ipadx = 2)
        self.okayButton.configure(state='disabled')
        buttonBar.columnconfigure("0 1 2", uniform = 'group1', weight = 1)

    def makeQandA(self):
        textFont = ('Helvetica', 12, 'bold')
        self.question = Label(self, bg = 'black', fg = 'yellow', font=textFont, width = 25, height = 1)
        self.question.grid(row = 1, column = 1, columnspan = 5, pady = 3)
        self.answer = Label(self, bg = 'black', fg = 'green', font=textFont, width = 25, height = 1)
        self.answer.grid(row = 2, column = 1, columnspan = 5, pady = 3)

    def highlight(self, target, start, end, tag, color, font):
        self.log.mark_set(INSERT, start)
        while(True):
            where = self.log.search(target, INSERT, end)
            if not where: break
            pastit = where + ('+%dc' % len(target))
            self.log.tag_add(tag, where, pastit)
            self.log.mark_set(INSERT, pastit)
        self.log.tag_config(tag, font = font, foreground = color)

    def makeLog(self):
        logFrame = Frame(self.parent)
        textFont = Font(family = 'Helvetica', size = 11)
        boldFont = Font(family = 'Helvetica', size = 11, weight = 'bold')
        errorFont = Font(family = 'Courier', size = 12)
        self.log = ScrolledText(logFrame, width = 60, height = 10, wrap = "none",
                                file='weekday.log', font = textFont, undo=True)
        self.log.text.bind("<Control-Key-x>", self.editCancelEvent)
        self.log.text.bind("<Control-Key-s>", self.editOkayEvent)
        self.log.text.bind("<Control-Key-z>", self.editUndo)
        self.log.text.bind("<Control-Key-y>", self.editRedo)
        self.log.text.tag_configure('error', font = errorFont)
        self.log.editing = False

        self.highlight('Correct', '1.0', END, 'correct', 'darkgreen', boldFont)
        self.highlight('Incorrect', '1.0', END, 'incorrect', 'red', boldFont)
        self.highlight('Time Expired', '1.0', END, 'expired', 'red', boldFont)

        text = self.log.gettext()
        right = text.count('Correct')
        wrong = text.count('Incorrect')
        expired = text.count('Expired')

        if right or wrong:
            pattern = re.compile(r'Time: (\d\d):(\d\d)')
            times = re.findall(pattern, text)
            minutes = sum((int(m) for (m,s) in times))
            seconds = sum((int(s) for (m,s) in times))
            avg = (60*minutes + seconds) / (right + wrong)
            self.log.append("\n%d correct % d incorrect Average time %.2f seconds\n" %
                            (right, wrong, avg))

        if expired:
            self.log.append("Time Limit Exceeded: %d\n" %expired)

        if right or wrong or expired:
            self.log.append('\n'+15*' ' + 'DO NOT DELETE THIS DASHED LINE\n')
            self.log.append(80*'-'+'\n')

        self.log.mark_set(INSERT, END)
        self.new =  self.log.index(INSERT)  # start here on output (onClose)
        self.log.configure(state='disabled')
        self.log.grid(row=0, column = 0, sticky = 'news')
        logFrame.grid(row=1, column = 0, sticky = 'news')
        logFrame.rowconfigure(0, weight = 1)
        self.parent.rowconfigure(1, weight = 1)

        buttonBar = Frame(logFrame, relief = FLAT, bd = 0)
        buttonBar.grid(row=1, column = 0, sticky=EW)
        self.okayEditButton = Button(buttonBar, text = 'Okay',relief = FLAT,
                                     command = self.editOkay)
        self.editButton = Button(buttonBar, text = 'Edit Log', relief = FLAT,
                                 command =  self.edit)
        self.cancelEditButton = Button(buttonBar, text = 'Cancel',relief = FLAT,
                                       command =  self.editCancel)
        self.okayEditButton.grid(pady = 3, column = 0, row = 0, ipadx = 2)
        self.editButton.grid(pady = 3, column = 1, row = 0, ipadx = 2)
        self.cancelEditButton.grid(pady = 3, column = 2, row = 0, ipadx = 2)
        buttonBar.columnconfigure("0 1 2", uniform = 'group2', weight = 1)
        self.okayEditButton.configure(state='disabled')
        self.cancelEditButton.configure(state='disabled')

    def go(self):
        self.answer.configure(text='')
        if self.year >= 0:
            self.question.configure(fg='yellow')
        else:
            self.question.configure(fg='orange')
        self.question.configure(text = self.dateString())
        self.playOff()
        self.watch.start()

    def playOn(self):
        self.okayButton.configure(state='disabled')
        self.playButton.configure(state='normal')
        self.setButton.configure(state='normal')
        self.editButton.configure(state='normal')

    def playOff(self):
        self.okayButton.configure(state='normal')
        self.playButton.configure(state='disabled')
        self.setButton.configure(state='disabled')
        self.editButton.configure(state='disabled')

    def play(self):
        self.answer.configure(text='')
        self.year = random.randint(self.minyear, self.maxyear)
        m = self.month = random.randint(1,12)
        if m == 2 and isLeap(self.year):
            self.day = random.randint(1, 29)
        else:
            self.day = random.randint(1, monthDays[m])
        self.go()

    def dateString(self):
        y = self.year
        m = self.month
        d = self.day
        return months[m]+" "+ str(d) +", "+ str(abs(y)) + (" A.D." if y >= 0 else " B.C.")

    def set(self):
        self.playOff()
        dialog = Toplevel(self.parent, width = 600)
        dialog.title("Input a Date")
        dialog.resizable(False, False)
        SetFrame(dialog, self).grid()
        self.alignPopup(dialog)

    def alignPopup(self, dialog):
        # Place the popup on top of the main app window

        geo = self.parent.wm_geometry()
        pattern = re.compile(r'(\d+x\d+)\+(\d+)\+(\d+)')
        wh1,x1,y1 = pattern.match(geo).groups()
        dialog.update_idletasks()
        geo = dialog.wm_geometry()
        wh2,x2,y2 = pattern.match(geo).groups()
        dialog.wm_geometry(wh2+'+'+x1+'+'+y1)

    def okay(self):
        self.watch.stop()
        y = self.year % 400 + 400
        weekday = date(y, self.month, self.day).isoweekday()
        response = self.response.get()
        correct = response == weekday
        color = 'green' if correct else 'red'
        self.answer.configure(text = days[response-1], fg = color)
        self.record(response, correct, weekday)
        self.playOn()

    def record(self, response, correct, weekday):
        text = self.dateString()
        time = self.watch.read()
        text += ' ' + days[response-1] + ' '
        text += 'Correct; ' if correct else 'Incorrect; '
        text += 'Time: ' + time +'\n'
        self.log.configure(state='normal')
        self.log.append(text)
        self.log.configure(state='disabled')
        if not correct:
            self.explain()
        time = 60*int(time[:-3]) + int(time[-2:])
        self.session.update(correct, int(time), expired=False)

    def explain(self):
        self.log.configure(state='normal')
        y = self.year % 400
        weekday = date(y, self.month, self.day).isoweekday()
        if y < 0: y += 400
        y100 = y // 100
        y1 = y % 100
        y4 = y1 // 4
        y5 = 5*y100;
        l = y4 + y1 + y5;
        delta = l % 7
        where = self.log.index(INSERT)
        self.log.append('  Year (mod 400): %d A.D.\n' % y)
        self.log.append('       Centuries: 5 * %d = %d\n' % (y100, y5))
        self.log.append('      Leap years: %d/4 = %d\n' % (y1, y4))
        self.log.append('           Delta: (%d + %d + %d) (mod 7) = %d\n' % ( y1, y4, y5, delta ))
        self.log.append('  Doomsday = %s; Weekday = %s\n\n' % (days[(1+delta) % 7], days[weekday-1]))
        self.log.tag_add('error', where, 'end - 1c')
        self.log.configure(state='disabled')

    def onTimeExpired(self, event):
        self.answer.configure(text = "Time Expired", fg = "yellow")
        self.playOn()
        text = self.dateString()
        text += 'Time Expired: %d seconds\n' %event.time
        self.log.configure(state='normal')
        self.log.append(text)
        self.log.configure(state='disabled')
        self.explain()
        self.session.update(correct=False, time=0, expired=True)

    def editOn(self):
        self.log.editing = True
        self.log.configure(bg='#ffffa6')
        self.editButton.configure(state = 'disabled')
        self.playButton.configure(state = 'disabled')
        self.setButton.configure(state = 'disabled')
        self.okayEditButton.configure(state = 'normal')
        self.cancelEditButton.configure(state = 'normal')
        self.log.configure(state = 'normal')

    def editOff(self):
        self.log.editing = False
        self.log.configure(bg='white')
        self.editButton.configure(state = 'normal')
        self.okayEditButton.configure(state = 'disabled')
        self.cancelEditButton.configure(state = 'disabled')
        self.log.configure(state = 'disabled')
        del self.oldText
        self.playButton.configure(state = 'normal')
        self.setButton.configure(state = 'normal')

    def edit(self):
        self.editOn()
        self.oldText = self.log.gettext()

    def editOkayEvent(self, event):
        if self.log.editing:
            self.editOkay()

    def editOkay(self):
        text = self.log.gettext()
        idx = text.find('----')
        if idx == -1:
            self.cancelEditButton.invoke()
            return
        with open('weekday.log', 'w') as fout:
            lines = text[:idx-1].split('\n')
            for line in lines:
                if line.find('Time') >= 0:
                    fout.write(line+'\n')
                elif line.endswith('M'):
                    fout.write('\n' + line + '\n')
        idx = self.log.search('---', '1.0')
        line = re.match(r'(\d+)\.\d+', idx).groups()[0]
        self.new = '%d.0' % (int(line)+1)
        self.log.edit_reset()       # clear undo stack
        self.editOff()
        self.playButton.focus_set()

    def editCancelEvent(self, event):
        if self.log.editing:
            self.editCancel()

    def editCancel(self):
        boldFont = Font(family = 'Helvetica', size = 11, weight = 'bold')
        self.log.settext(self.oldText)
        self.highlight('Correct', '1.0', self.new, 'correct', 'darkgreen', boldFont)
        self.highlight('Incorrect', '1.0', self.new, 'incorrect', 'red', boldFont)
        self.highlight('Time Expired', '1.0', self.new, 'expired', 'red', boldFont)
        self.editOff()

    def editUndo(self, event):
        if self.log.editing:
            self.log.edit_undo()

    def editRedo(self, event):
        if self.log.editing:
            self.log.edit_redo()

    def onClose(self):
        now = datetime.now()
        lines = self.log.gettext(self.new).split('\n')
        if len(lines) > 1:
            with open('weekday.log','a') as fout:
                fout.write(now.strftime('\n%A, %d %B %Y %I:%M %p\n'))
                for line in lines:
                    if line.find('Time') >= 0:
                        fout.write(line+'\n')
        with open('weekday.ini', 'w') as fout:
            fout.write('self.minyear = %d\n' %self.minyear)
            fout.write('self.maxyear = %d\n' % self.maxyear)
            fout.write('self.timeout = %d\n' %self.timeout)
        self.parent.destroy()

    def map(self, event):
        timer = self.watch
        if timer.state == 'paused':
            timer.resume()

    def unmap(self, event):
        timer = self.watch
        if timer.state == 'running':
            timer.pause()

    def helpAlgorithm(self):
        from help import algorithmText
        helpFont = Font(family = 'Helevetica', size = '12')
        win = Toplevel()
        win.title('Weekday Help')
        text = ScrolledText(win, wrap= WORD)
        text.configure(font = helpFont)
        text.append(algorithmText)
        text.configure(state=DISABLED)
        ok = Button(win, text='Okay', command = win.destroy)
        text.pack(expand=YES, fill = BOTH)
        ok.pack()
        text.see('1.0')

    def about(self):
        showinfo("Notice","The author has placed this code in the public domain.")

    def getYearSettings(self):
        dialog = Toplevel()
        dialog.title("Generated Years")
        settings = YearDialog(dialog, self)
        settings.grid()
        dialog.resizable(False, False)
        self.alignPopup(dialog)

    def getTimeoutSettings(self):
        dialog = Toplevel()
        dialog.title("Time Limit")
        settings = TimeoutDialog(dialog, self)
        settings.grid()
        dialog.resizable(False, False)
        self.alignPopup(dialog)

class SessionStats(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.correct = StringVar()
        self.incorrect = StringVar()
        self.expired = StringVar()
        self.average = StringVar()
        self.totalTime = 0
        c = LabelFrame(self, text = "Number Correct")
        ce = Label(c, textvariable = self.correct)
        ce.grid(sticky = "ew")
        c.grid(row = 0, column = 0, sticky = "ew")
        i = LabelFrame(self, text = "Number Incorrect")
        ie = Label(i, textvariable = self.incorrect)
        ie.grid(sticky = "ew")
        i.grid(row = 0, column = 1, sticky = "ew")
        t = LabelFrame(self, text = "Time Expired")
        te = Label(t, textvariable = self.expired)
        te.grid(sticky = "ew")
        t.grid(row = 0, column = 2, sticky = "ew")
        a = LabelFrame(self, text = "Average Time")
        ae = Label(a, textvariable = self.average)
        ae.grid(sticky = "ew")
        a.grid(row = 0, column = 3, sticky = "ew")
        self.columnconfigure("0 1 2 3", uniform = 'group1', weight = 1)

        self.correct.set("0")
        self.incorrect.set("0")
        self.expired.set("0")

    def update(self, correct, time, expired = False):
        if not expired:
            self.totalTime += time
            right = int(self.correct.get())
            wrong = int(self.incorrect.get())
            right += correct
            wrong += not correct
            self.correct.set(str(right))
            self.incorrect.set(str(wrong))
            total = right + wrong
            average = self.totalTime/(right+wrong)
            self.average.set("%.2f" % average)
        else:
            expired = int(self.expired.get())
            self.expired.set(str(expired+1))

class ValidatedEntry(LabelFrame):
    # for validation documentation, see
    # http://stackoverflow.com/questions/4140437/python-tkinter-interactively-validating-entry-widget-content

    def __init__(self, parent, title, valid, **kwargs):
        LabelFrame.__init__(self, parent, text = title);
        self.valid=valid
        cmd = (self.register(self.validate), "%P")
        self.entry = Entry(self, validate="key", validatecommand=cmd, **kwargs)
        self.entry.grid(sticky=EW)

    # ValidatedEntry is a proxy for the included Entry

    def focus_set(self):
        self.entry.focus_set()

    def __getattr__(self, name):
        return getattr(self.entry, name)

    def validate(self, proposed):
        return all([c in self.valid for c in proposed])

class SetFrame(Frame):
    def __init__(self, parent, target):
        Frame.__init__(self, parent)
        self.parent = parent
        self.target = target
        self.year = ValidatedEntry(self, 'Year', '0123456789', width = 12)
        self.month = ValidatedEntry(self, 'Month', '0123456789', width = 12)
        self.day = ValidatedEntry(self, 'Day', '0123456789', width = 12)
        self.year.grid(row = 0, pady = 3, padx = 5)
        self.month.grid(row = 1, pady = 3, padx = 5)
        self.day.grid(row = 2, pady = 3, padx = 5)

        buttonBar = Frame(self, relief = FLAT, bd = 0)
        okay = Button(buttonBar, text='Okay', command = self.getDate)
        cancel = Button(buttonBar, text = 'Cancel', command=self.cancel)
        okay.grid(padx = 5, column = 0, row = 0)
        cancel.grid(padx = 5, column = 0, row = 1)
        buttonBar.grid(row = 1, column = 1, rowspan = 2, padx = 5, sticky = NS)
        buttonBar.rowconfigure("0 1", uniform = 'group1', weight = 1)
        self.year.focus_set()

        buttonBar = Frame(self,relief = FLAT, bd = 0)
        buttonBar.grid(row=0, column = 1, sticky=EW)
        buttonBar.columnconfigure("0 1", uniform = 'all', weight = 1)
        self.era = IntVar()
        self.era.set(1)
        ad = Radiobutton(buttonBar, text='A.D.', variable = self.era, value = 1)
        bc = Radiobutton(buttonBar, text='B.C.', variable = self.era, value = -1)
        ad.grid(row = 0, column = 0)
        bc.grid(row = 0, column = 1)

        self.message = Label(self, text ='', fg = 'red')
        self.message.grid(row = 3, column = 0, columnspan = 2, sticky = 'news')
        parent.wm_protocol("WM_DELETE_WINDOW", self.cancel)

    def getDate(self):
        try:
            y = int(self.year.get())
        except ValueError:
            self.message.configure(text='Invalid year')
            self.year.focus_set()
            return
        try:
            m = int(self.month.get())
        except ValueError:
            self.message.configure(text='Invalid month')
            self.month.focus_set()
            return
        try:
            d = int(self.day.get())
        except ValueError:
            self.message.configure(text='Invalid day')
            self.day.focus_set()
            return
        self.message.configure(text='')
        if not ( 1 <= m <= 12):
            self.message.configure(text='Invalid month')
            self.month.focus_set()
            return
        good = True
        if isLeap(y) and m == 2:
            if d > 29:
                good = False
        elif d >monthDays[m]:
            good = False
        if not good:
            self.message.configure(text='Invalid day')
            self.day.focus_set()
            return
        y *= self.era.get()
        self.target.year = y
        self.target.month = m
        self.target.day = d
        self.target.go()
        self.parent.destroy()

    def cancel(self):
        target = self.target
        target.okayButton.configure(state='disabled')
        target.playButton.configure(state='normal')
        target.setButton.configure(state='normal')
        target.editButton.configure(state='normal')
        self.parent.destroy()

class YearDialog(Frame):
    def __init__(self, parent, board):
        Frame.__init__(self, parent)
        maxvar = StringVar()
        maxvar.set(str(board.maxyear))
        minvar = StringVar()
        minvar.set(str(board.minyear))
        minEntry = ValidatedEntry(self, 'Minimum Year', '-0123456789', textvariable=minvar, width = 10)
        minEntry.grid(row = 0, column = 0, pady = 2, padx = 4)
        maxEntry = ValidatedEntry(self, 'Maximum Year', '-0123456789', textvariable=maxvar, width = 10)
        maxEntry.grid(row = 0, column = 1, pady = 2, padx = 4)
        ok = Button(self, text = "Okay", command = self.okay)
        ok.grid(row = 1, column = 0, padx = 3, pady = 2)
        cancel = Button(self, text = "Cancel", command = self.cancel)
        cancel.grid(row = 1, column = 1, padx = 3, pady = 2)
        self.message = Label(self, text ='', fg = 'red')
        self.message.grid(row = 2, column = 0, columnspan = 2, sticky = 'news')
        self.minEntry = minEntry
        self.maxEntry = maxEntry
        self.board = board
        minEntry.focus_set()

    def cancel(self):
        self.winfo_toplevel().destroy()

    def okay(self):
        try:
            minyear = int(self.minEntry.get())
        except ValueError:
            self.message.configure(text = 'Invalid minimum year')
            self.minEntry.focus_set()
            return
        try:
            maxyear = int(self.maxEntry.get())
        except ValueError:
            self.message.configure(text = 'Invalid maximum year')
            self.maxEntry.focus_set()
            return
        if minyear > maxyear:
            self.message.configure(text = 'Minimum greater than maximum')
            self.maxEntry.focus_set()
            return
        self.board.minyear = minyear
        self.board.maxyear = maxyear
        self.winfo_toplevel().destroy()

class TimeoutDialog(Frame):
    def __init__(self, parent, board):
        Frame.__init__(self, parent)
        timevar = StringVar()
        timevar.set(str(board.timeout))
        timeEntry = ValidatedEntry(self, 'Seconds', '0123456789', textvariable=timevar, width = 6)
        l = Label(self, text = '0 = No Limit')
        l.grid(row = 0, column = 1, pady = 2, padx = 4)
        timeEntry.grid(row = 0, column = 0, pady = 2, padx = 4)
        ok = Button(self, text = "Okay", command = self.okay)
        ok.grid(row = 1, column = 0, padx = 3, pady = 2)
        cancel = Button(self, text = "Cancel", command = self.cancel)
        cancel.grid(row = 1, column = 1, padx = 3, pady = 2)
        self.time = timeEntry
        self.board = board
        timeEntry.focus_set()

    def cancel(self):
        self.winfo_toplevel().destroy()

    def okay(self):
        self.board.timeout = int(self.time.get())
        self.board.watch.setLimit(self.board.timeout)
        self.winfo_toplevel().destroy()

if __name__ == '__main__':
    root = Tk()
    root.resizable(False, True)
    root.title("Day of the Week")
    app = Board(root)
    root.mainloop()
