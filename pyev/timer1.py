#!/usr/bin/env python
# vim: set ai tw=79 sw=4 ts=4 sta et fo=croql:

import pyev

class FiveSecondTimer(object):
    def __init__(self, data):
        self.data = data

    def __call__(self, watch, revents):
        print 'foo', self.data

loop = pyev.default_loop()
run_every_5_seconds = FiveSecondTimer([1, 2, 3])
run_every_5_seconds_loop = loop.timer(0, 5, run_every_5_seconds)
run_every_5_seconds_loop.start()
loop.start()


