# Simple python threadpool implementation from
# http://code.activestate.com/recipes/577187-python-thread-pool/

# {{{ http://code.activestate.com/recipes/577187/ (r9)

from threading import Thread

from six.moves.queue import Queue


class Worker(Thread):
    """Thread executing tasks from a given tasks queue."""

    def __init__(self, tasks):
        Thread.__init__(self)
        self.tasks = tasks
        self.daemon = True
        self.start()

    def run(self):
        """Run the worker thread."""
        while True:
            func, args, kargs = self.tasks.get()
            try:
                func(*args, **kargs)
            except Exception as e:
                print(e)
            self.tasks.task_done()


class ThreadPool:
    """Pool of threads consuming tasks from a queue."""

    def __init__(self, num_threads):
        self.tasks = Queue(num_threads)
        for _ in range(num_threads):
            Worker(self.tasks)

    def add_task(self, func, *args, **kargs):
        """Add a task to the queue."""
        self.tasks.put((func, args, kargs))

    def wait_completion(self):
        """Wait for completion of all the tasks in the queue."""
        self.tasks.join()


# end of http://code.activestate.com/recipes/577187/ }}}
