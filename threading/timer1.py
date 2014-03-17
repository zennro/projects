#!/usr/bin/env python
from time import sleep
from threading import Timer

def hello():
	print "hello world"
	sleep(2)

t = Timer(3.0, hello)
t.start()

