# based on FramePack https://github.com/lllyasviel/FramePack

import time
import traceback

from threading import Thread, Lock, Condition


class Listener:
    task_queue = []
    lock = Lock()
    condition = Condition(lock)
    thread = None
    
    @classmethod
    def _process_tasks(cls):
        while True:
            task = None
            with cls.condition:
                while not cls.task_queue:
                    cls.condition.wait()
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
        with cls.condition:
            cls.task_queue.append((func, args, kwargs))
            cls.condition.notify()

        if cls.thread is None:
            cls.thread = Thread(target=cls._process_tasks, daemon=True)
            cls.thread.start()


def async_run(func, *args, **kwargs):
    Listener.add_task(func, *args, **kwargs)


class FIFOQueue:
    def __init__(self):
        self.queue = []
        self.lock = Lock()
        self.condition = Condition(self.lock)

    def push(self, cmd, data = None):
        with self.condition:
            self.queue.append( (cmd, data) )
            self.condition.notify()

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
        with self.condition:
            while not self.queue:
                self.condition.wait()
            return self.queue.pop(0)


class AsyncStream:
    def __init__(self):
        self.input_queue = FIFOQueue()
        self.output_queue = FIFOQueue()
