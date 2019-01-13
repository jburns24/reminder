import gi, sys, time, os
gi.require_version('Notify', '0.7')
from gi.repository import Notify
from signal import SIGTERM
from daemon import Daemon
from time_converter import TimeConverter

## To Do chang the daemon to only open the file and read in lines if the
## last modified time is different. 

# Subclass for daemon this will read from the reminder_log
# read all lines in the reminder log and if the current time
# equals one of the reminder times send that reminder.
# then removes that line
class RDaemon(Daemon):
        def run(self):
                while True:
                    try:
                        f = open(self.logfile, "r+")
                        lines = f.readlines()
                        f.seek(0) # put buffer at front
                        for line in lines:
                            line_ar = line.split()
                            if int(line_ar[0]) == int(time.time()):
                                Notify.init('Remind Me')
                                notification = Notify.Notification.new('REMINDER', ' '.join(line_ar[1:]))
                                notification.show()
                            else:
                                f.write(line)
                        f.truncate()
                        f.close()
                    except IOError:
                        print("no reminder log")
                    # Notify.init('Remind Me')
                    # notification = Notify.Notification.new('REMINDER', test)
                    # notification.show()
                    # time.sleep(10)

        def stop(self):
                """
                Stop the daemon
                """
                # Get the pid from the pidfile
                try:
                        pf = file(self.pidfile,'r')
                        pid = int(pf.read().strip())
                        pf.close()
                except IOError:
                        pid = None
        
                if not pid:
                        message = "pidfile %s does not exist. Daemon not running?\n"
                        sys.stderr.write(message % self.pidfile)
                        return # not an error in a restart
    
                # Try killing the daemon process       
                try:
                        while 1:
                                Notify.uninit()
                                os.kill(pid, SIGTERM)
                                time.sleep(0.1)
                except OSError, err:
                        err = str(err)
                        if err.find("No such process") > 0:
                                if os.path.exists(self.pidfile):
                                        os.remove(self.pidfile)
                        else:
                                print str(err)
                                sys.exit(1)        