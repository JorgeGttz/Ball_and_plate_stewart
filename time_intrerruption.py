#!/usr/bin/env python
# simple example of threading.Timer in python

import time, threading

class ticker(object):
    def __init__(self, initial = 0, update_interval = 0.001):
        self.ticker = initial
        self.update_interval = update_interval

    def init(self):
        self.ticker += 1
        # Timer only runs once so call recursively in inc()
        threading.Timer(self.update_interval, self.init).start()

a = ticker()
a.init() # increment counter and start timer thread in each object

while True:
    # loop forever
    time.sleep(0.001)
    print ("a={}".format(a.ticker))
    if(a.ticker>10):   a.ticker=0
    
