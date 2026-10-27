# based on FramePack https://github.com/lllyasviel/FramePack

import time
import traceback
from collections import deque

from threading import Thread, Lock, Condition


class Listener:
    task_queue = deque()
    lock = Lock()
    cond = Condition(lock)
    thread = None
    
    @classmethod
    def _process_tasks(cls):
        while True:
            task = None
            # ⚡ Bolt Optimization: Use condition variables (wait/notify) instead of polling
            # with time.sleep() to reduce background idle CPU usage to ~0%.
            with cls.cond:
                while not cls.task_queue:
                    cls.cond.wait()
                # ⚡ Bolt Optimization: Use collections.deque for O(1) popleft() instead of list pop(0)
                task = cls.task_queue.popleft()
                
            func, args, kwargs = task
            try:
                func(*args, **kwargs)
            except Exception as e:
                tb = traceback.format_exc().split('\n')[:-1] 
                print('\n'.join(tb))

                # print(f"Error in listener thread: {e}")
    
    @classmethod
    def add_task(cls, func, *args, **kwargs):
        with cls.cond:
            cls.task_queue.append((func, args, kwargs))
            cls.cond.notify()

        if cls.thread is None:
            cls.thread = Thread(target=cls._process_tasks, daemon=True)
            cls.thread.start()


def async_run(func, *args, **kwargs):
    Listener.add_task(func, *args, **kwargs)


class FIFOQueue:
    def __init__(self):
        self.queue = deque()
        self.lock = Lock()
        self.cond = Condition(self.lock)

    def push(self, cmd, data = None):
        with self.cond:
            self.queue.append( (cmd, data) )
            self.cond.notify()

    def pop(self):
        with self.cond:
            if self.queue:
                # ⚡ Bolt Optimization: Use collections.deque for O(1) popleft() instead of list pop(0)
                return self.queue.popleft()
            return None

    def top(self):
        with self.cond:
            if self.queue:
                return self.queue[0]
            return None

    def next(self):
        with self.cond:
            while not self.queue:
                self.cond.wait()
            # ⚡ Bolt Optimization: Use collections.deque for O(1) popleft() instead of list pop(0)
            return self.queue.popleft()


class AsyncStream:
    def __init__(self):
        self.input_queue = FIFOQueue()
        self.output_queue = FIFOQueue()
