try:
    from tkinter import *
except ImportError:
    from Tkinter import *
import time

# A StopWatch object may have a time limit.  If this limit expires, the watch
# stops and triggers a <<TimeLimitExpired>> virtual event.

class StopWatch(Frame):
    def __init__(self, win, limit = 0):
        Frame.__init__(self, win)
        self.text = StringVar()
        self.label = Label(self, textvariable=self.text)
        timeFont = ('helevetica', 12, 'bold')
        self.label.config(bd=4, relief=SUNKEN, bg='black', fg = 'yellow', text='00:00', font = timeFont)
        self.state = 'waiting'
        self.afterID = 0
        self.label.pack()
        self.limit = limit
        self.event_add('<<TimeLimitExpired>>', '<Triple-Key-Pause>')
        # These next 3 lines just set the initial display
        # self.startTime is reset when the watch starts
        self.startTime = time.time()
        self.onTimer()
        self.stop()

    def start(self):
        self.startTime = time.time()
        self.state = 'running'
        self.label.config(fg = 'green')
        self.onTimer()

    def stop(self):
        if self.state == 'running':
            self.after_cancel(self.afterID)
        self.label.configure(fg = 'red')
        self.state = 'stopped'

    def setLimit(self, limit):
        self.limit = limit

    def onTimer(self):
        elapsed = int(time.time() - self.startTime)
        if elapsed >= 3600:
            hours = elapsed // 3600
            elapsed -= 3600*hours
            minutes = elapsed // 60
            seconds = elapsed % 60
            timeText = '%d:%02d:%02d' % (hours, minutes, seconds)
        else:
            minutes = elapsed // 60
            seconds = elapsed % 60
            timeText = '%02d:%02d' % (minutes, seconds)
        self.text.set(timeText)
        if elapsed >= self.limit > 0:
            self.stop()
            self.event_generate('<<TimeLimitExpired>>', time=self.limit)
        if self.state == 'running':
            self.afterID = self.after(100, self.onTimer)

    def pause(self):
        self.after_cancel(self.afterID)
        self.label.configure(fg = 'yellow')
        self.elapsedTime = time.time() - self.startTime
        self.state = 'paused'

    def resume(self):
        self.startTime = time.time() - self.elapsedTime
        self.label.config(fg = 'green')
        self.state = 'running'
        self.onTimer()

    def time(self):
        return time.time() - self.startTime

    def setTime(self, seconds):
        self.elapsedTime = seconds

    def read(self):
        return self.text.get()

if __name__ == '__main__':
    def catch(event): print("Caught")
    root = Tk()
    watch=StopWatch(root)
    f = Frame(root)
    watch.pack()
    f.pack()
    f.bind_all('<<TimeLimitExpired>>', catch)
    watch.setLimit(10)
    watch.start()
    root.mainloop()
