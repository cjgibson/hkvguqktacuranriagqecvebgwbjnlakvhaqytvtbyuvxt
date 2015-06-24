###
# AUTHORS: CHRISTIAN GIBSON, 
# PROJECT: REDDIT CHALLENGES
# UPDATED: FEBURARY 28, 2015
# USAGE:   
# EXPECTS: python 2.7.6
###

task = """
Your mission is to create a stopwatch program. this program should have
start, stop, and lap options, and it should write out to a file to be viewed
later.
"""

import Tkinter
import time
import os

class stopwatch(Tkinter.Tk):
    def __init__(self, capture_key='s', filename='timer.csv', *args, **kwargs):
        Tkinter.Tk.__init__(self, *args, **kwargs)
        if not os.path.isfile(filename):
            self.filehandle = open(filename, 'w')
            self.filehandle.write('Elapsed_Time,Start_Time,End_Time\n')
        else:
            self.filehandle = open(filename, 'a')
        self.started = False
        self.start_t = None
        self.capture = capture_key
        print "Pressing <%s> will start the stopwatch." % self.capture
        print "Pressing <%s> again will stop it." % self.capture
        print "Press <Esc> to quit."
        self.bind('<Key>', self.keypress)
        self.mainloop()
    
    def keypress(self, event):
        if event.char == self.capture:
            if self.started:
                end_t = time.time()
                elapsed = (end_t - self.start_t)
                print 'Stopwatch Stopped.'
                print 'Elapsed time: %f seconds.' % (elapsed)
                self.filehandle.write('%f,%f,%f\n'
                                      % (elapsed,
                                         self.start_t,
                                         end_t))
                self.started = False
                self.start_t = None
            else:
                self.started = True
                self.start_t = time.time()
                print 'Stopwatch Started.'
        if event.keysym == 'Escape':
            self.destroy()
            self.filehandle.close()

if __name__ == '__main__':
    stopwatch = stopwatch()