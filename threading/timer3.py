#!/usr/bin/env python

import threading

def ontimer():
    print threading.current_thread()

def main():
    timer = threading.Timer(2, ontimer)
    timer.start()
    print threading.current_thread()
    timer.cancel()
    timer.join()         # here you block the main thread until the timer is completely stopped
    if timer.isAlive():
        print "Timer is still alive"
    else:
        print "Timer is no more alive"
    if timer.finished:
        print "Timer is finished"


if __name__ == "__main__":
	main()
