import subprocess
import select

poller = select.epoll()
subprocs = {} #map stdout pipe's file descriptor to the Popen object

#spawn some processes
for i in xrange(5):
    subproc = subprocess.Popen(["mylongrunningproc"], stdout=subprocess.PIPE)
    subprocs[subproc.stdout.fileno()] = subproc
    poller.register(subproc.stdout, select.EPOLLHUP)

#loop that polls until completion
while True:
    for fd, flags in poller.poll(timeout=1): #never more than a second without a UI update
        done_proc = subprocs[fd]
        poller.unregister(fd)
        print "this proc is done! blah blah blah"
          #do whatever
    #print a reassuring spinning progress widget
    #...
    #don't forget to break when all are done
