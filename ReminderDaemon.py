import gi, sys, time, os
gi.require_version('Notify', '0.7')
from gi.repository import Notify
from signal import SIGTERM
from daemon import Daemon
from time_converter import TimeConverter

# Subclass for daemon this will read from the reminder_log
# read all lines in the reminder log and if the current time
# equals one of the reminder times send that reminder.
# then removes that line
class RDaemon(Daemon):
        def run(self):
            try:
                lastModified = int(os.path.getmtime(self.logfile))
                pastReminders = []
                f = open(self.logfile, "r+")
                lines = f.readlines()
                f.close()
                Notify.init('Remind Me')
            except OSError:
                print("no reminder log")
                self.stop()

            while True:
                # if last modified is different than the last time daemon
                # grabbed the lines we need to update local reminders
                if lastModified != int(os.path.getmtime(self.logfile)):
                    f = open(self.logfile, "r+")
                    lines = f.readlines()
                    f.close()
                    lastModified = int(os.path.getmtime(self.logfile))

                # scan all the local reminders to see if one needs to be executed
                for line in lines:
                    line_ar = line.split()
                    if int(line_ar[0]) == int(time.time()):
                        notification = Notify.Notification.new('REMINDER', ' '.join(line_ar[1:]))
                        notification.show()
                        pastReminders.append(line)

                # if we have past reminders clean them up and update local lines
                if pastReminders:
                    f = open(self.logfile, "r+")
                    # lines = f.readlines()
                    f.seek(0) # put buffer at front
                    for line in lines:
                        if line not in pastReminders:
                            f.write(line)
                    f.truncate()
                    lines = f.readlines()
                    f.close()
                    lastModified = int(os.path.getmtime(self.logfile))
                    pastReminders = []
                time.sleep(5)


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