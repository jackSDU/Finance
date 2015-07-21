from multiprocessing import Process
from Server.server import cmd_read,stop_read,worker_daemon

p=Process(target = worker_daemon, args=(cmd_read,stop_read))
p.daemon=True
p.start()

from Server.server import app as application