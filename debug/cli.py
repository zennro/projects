#!/usr/bin/python3.2

import pyev
import sys

class cli:
	def __init__(self, loop):
		sys.ps1 = ">>>"
		sys.ps2 = "..."

		import ctypes
		libc = ctypes.cdll.LoadLibrary("libc.so.6")
		libc.fdopen.restype = ctypes.c_void_p
		libc.fdopen.argtype = [ctypes.c_int, ctypes.c_char_p]
		self.stdin = libc.fdopen(sys.stdin.fileno(),"r")
		self._io = pyev.Io(sys.stdin.fileno(), pyev.EV_READ, loop, self._io_cb)
		self._io.start()

		import termios
		# [iflag, oflag, cflag, lflag, ispeed, ospeed, cc] 
		self.read_termios = termios.tcgetattr(sys.stdin.fileno());
		self.poll_termios = termios.tcgetattr(sys.stdin.fileno());

		self.read_termios[3] |=  (termios.ICANON|termios.ECHOCTL|termios.ECHO);
		self.poll_termios[3] &= ~(termios.ICANON|termios.ECHOCTL|termios.ECHO);

		try:
			import readline
		except ImportError:
			print("Module readline not available.")
		else:
			import rlcompleter
			readline.parse_and_bind("tab: complete")

		import atexit
		atexit.register(self._atexit)

	def _atexit(self):		
		self.mode(self.read_termios)

	def setblocking(self,blocking):
		import fcntl
		import os
		if blocking == True:
			fcntl.fcntl(sys.stdin.fileno(), fcntl.F_SETFL, fcntl.fcntl(sys.stdin.fileno(), fcntl.F_GETFL) | os.O_NONBLOCK)
		else:
			fcntl.fcntl(sys.stdin.fileno(), fcntl.F_SETFL, fcntl.fcntl(sys.stdin.fileno(), fcntl.F_GETFL) & ~os.O_NONBLOCK)

	def mode(self, m):
		import termios
		termios.tcsetattr(sys.stdin.fileno(), termios.TCSANOW, m)

	def _io_cb(self, watcher, revents):
		from ctypes import pythonapi
		self.mode(self.read_termios)
#		self.setblocking(False)
#		nonblocking stdin causes very interesting problems here!

		pythonapi.PyRun_InteractiveOne(self.stdin, b"<stdin>")

#		self.setblocking(True)
#		even if disabled during runtime operation

		self.mode(self.poll_termios)

if __name__ == '__main__':
	loop = pyev.default_loop()
	c = cli(loop)

	def signals(watcher, revents):
		watcher.loop.stop()

	import signal
	sigint = pyev.Signal(signal.SIGINT, loop, signals)
	sigint.start()

	loop.start()
	sys.exit(0)