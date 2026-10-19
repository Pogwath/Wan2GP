# based on FramePack https://github.com/lllyasviel/FramePack

import time
import traceback

from threading import Thread, Lock, Condition


class _TaskRunner:
    def __init__(self, runner_name="default"):
        self.runner_name = str(runner_name or "default")
        self.thread_name = self.runner_name.replace("_", " ").strip().title() or "Default"
        self.task_queue = []
        self.lock = Lock()
        self.condition = Condition(self.lock)
        self.thread = None

    def _process_tasks(self):
        """
        Processes tasks from the queue.
        Optimized to use Condition variables instead of busy-waiting (time.sleep(0.001)).
        This drops idle CPU usage of background threads to zero.
        """
        while True:
            with self.lock:
                while not self.task_queue:
                    self.condition.wait()
                task = self.task_queue.pop(0)
                
            func, args, kwargs, thread_name = task
            current_name = None
            thread = self.thread
            try:
                if thread_name and thread is not None:
                    current_name = thread.name
                    thread.name = thread_name
                func(*args, **kwargs)
            except Exception as e:
                tb = traceback.format_exc().split('\n')[:-1] 
                print('\n'.join(tb))

                # print(f"Error in listener thread: {e}")
            finally:
                if current_name is not None and thread is not None:
                    thread.name = current_name

    def add_task(self, func, *args, thread_name=None, **kwargs):
        with self.lock:
            self.task_queue.append((func, args, kwargs, thread_name))
            self.condition.notify()
            thread = None if self.thread is not None else Thread(target=self._process_tasks, daemon=True, name=self.thread_name)
            if thread is not None:
                self.thread = thread

        if thread is not None:
            thread.start()


class Listener:
    runners = {}
    lock = Lock()

    @classmethod
    def _get_runner(cls, runner_name="default"):
        runner_name = str(runner_name or "default")
        with cls.lock:
            runner = cls.runners.get(runner_name, None)
            if runner is None:
                runner = _TaskRunner(runner_name)
                cls.runners[runner_name] = runner
            return runner

    @classmethod
    def add_task(cls, func, *args, runner_name="default", thread_name=None, **kwargs):
        cls._get_runner(runner_name).add_task(func, *args, thread_name=thread_name, **kwargs)


def async_run(func, *args, thread_name=None, **kwargs):
    Listener.add_task(func, *args, thread_name=thread_name, **kwargs)


def async_run_in(runner_name, func, *args, thread_name=None, **kwargs):
    Listener.add_task(func, *args, runner_name=runner_name, thread_name=thread_name, **kwargs)


class FIFOQueue:
    def __init__(self):
        self.queue = []
        self.lock = Lock()
        self.condition = Condition(self.lock)

    def push(self, cmd, data = None):
        with self.lock:
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
        """
        Waits for the next item in the queue.
        Optimized to use Condition variables instead of busy-waiting.
        """
        with self.lock:
            while not self.queue:
                self.condition.wait()
            return self.queue.pop(0)


class AsyncStream:
    def __init__(self):
        self.input_queue = FIFOQueue()
        self.output_queue = FIFOQueue()
