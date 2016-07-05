import os

from nullmailer_lib import HandleRequest
from rabbit2ev.exception import (
    NullMailerErrorPool,
    NullMailerErrorPipe
)


class NullMailer(object):

    tmp = "/var/spool/nullmailer/tmp"
    queue = "/var/spool/nullmailer/queue"
    trigger = "/var/spool/nullmailer/trigger"
    __counter = 0
    __pid = os.getpid()

    def fsync_pool(self):
        """
        Call fsync() on the queue directory
        """
        fd = -1
        if not os.path.isdir(self.queue) or not os.access(self.queue, os.R_OK):
            raise NullMailerErrorPool(
                "%s' not exist or inaccesible" % self.queue)

        try:
            fd = os.open(self.queue, os.O_RDONLY)
            os.fsync(fd)
        except Exception as e:
            raise NullMailerErrorPool(e)
        finally:
            if fd > -1:
                os.close(fd)

    def trigger_pipe(self):
        """
        Wakeup nullmailer writing to its trigger fifo
        """
        fd = -1
        try:
            fd = os.open(self.trigger, os.O_WRONLY | os.O_NONBLOCK)
            os.write(fd, "\0")
        except Exception as e:
            raise NullMailerErrorPipe(e)
        finally:
            if fd > -1:
                os.close(fd)

    def sendmail(self, data):
        self.__counter += 1
        r = HandleRequest(self.tmp, self.queue, self.__counter)

        try:
            r.start(data)
            os.link(r.tmp_file, r.spool_file)
            self.fsync_pool()
            self.trigger_pipe()
        except Exception:
            raise
        finally:
            os.unlink(r.tmp_file)
            r.tearDown()
