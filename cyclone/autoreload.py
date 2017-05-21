import os, sys, subprocess, threading, time
from apscheduler.schedulers.background import BackgroundScheduler 

from twisted.internet import reactor  

sched = BackgroundScheduler()
sched.start()

_reload_attempted = False
modify_times = {}

def start():
	sched.add_job(_reload_on_update, 'interval', seconds=.5, id="poll")

def _reload_on_update():
	for module, m in sys.modules.items():
		if m is None:
			continue
		if getattr(m, '__file__', None) is None:
			continue

		result = _check_file(m.__file__.lower()) 
		if result != None:
			print("Detected a change in " + str(result) + "\nRestarting " + str(sys.argv[0])) 
			_reload()

def _check_file(path): 
	try:
		modified = os.stat(path).st_mtime
	except Exception:
		return None

	if path not in modify_times:
		modify_times[path] = modified
		return None

	if modify_times[path] != modified:
		return path
 
def _reload(): 
	sched.remove_job("poll")
	reactor.callWhenRunning(reactor.stop)
	time.sleep(1)
	subprocess.Popen([sys.executable] + sys.argv, shell=True)
