# based on FramePack https://github.com/lllyasviel/FramePack

import time
import traceback

from threading import Thread, Lock


class Listener:
    task_queue = []
    lock = Lock()
    cond = __import__("threading").Condition(lock)
    thread = None
    
    @classmethod
    def _process_tasks(cls):
        while True:
            task = None
            with cls.lock:
                while not cls.task_queue:
                    cls.cond.wait()
                task = cls.task_queue.pop(0)
                
            func, args, kwargs = task
            try:
                func(*args, **kwargs)
            except Exception as e:
                tb = traceback.format_exc().split('\n')[:-1] 
                print('\n'.join(tb))

                # print(f"Error in listener thread: {e}")
    
    @classmethod
    def add_task(cls, func, *args, **kwargs):
        """
        ⚡ Bolt: Thread wait performance improvement
        💡 What: Replaced busy-waiting loops with `threading.Condition` blocking `wait()` and `notify()`.
        🎯 Why: Background thread polling loops using `time.sleep()` for waiting on queues consume CPU cycles unnecessarily by repeatedly waking up, checking the queue, and sleeping. This eliminates busy waiting overhead and gives exactly 0% idle CPU usage.
        """
        with cls.lock:
            cls.task_queue.append((func, args, kwargs))
            cls.cond.notify()

        if cls.thread is None:
            cls.thread = Thread(target=cls._process_tasks, daemon=True)
            cls.thread.start()


def async_run(func, *args, **kwargs):
    Listener.add_task(func, *args, **kwargs)


class FIFOQueue:
    def __init__(self):
        self.queue = []
        self.lock = Lock()
        self.cond = __import__("threading").Condition(self.lock)

    def push(self, cmd, data = None):
        with self.lock:
            self.queue.append( (cmd, data) )
            self.cond.notify()

    def pop(self):
        with self.lock:
            if self.queue:
                return self.queue.pop(0)
            return None

    def top(self):
        with self.lock:
            if self.queue:
                return self.queue[0]
            return None

    def next(self):
        """
        ⚡ Bolt: FIFOQueue wait performance improvement
        💡 What: Replaced polling with `threading.Condition` blocking `wait()`
        🎯 Why: Replaced busy wait (`time.sleep(0.001)`) which constantly wakes thread and wastes CPU time, with zero-CPU condition waiting.
        """
        with self.lock:
            while not self.queue:
                self.cond.wait()
            return self.queue.pop(0)


class AsyncStream:
    def __init__(self):
        self.input_queue = FIFOQueue()
        self.output_queue = FIFOQueue()
