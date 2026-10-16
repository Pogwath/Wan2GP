
## 2024-10-16 - Eliminate busy-waiting in background threads
**Learning:** Background thread polling mechanisms (like `Listener` and `FIFOQueue` in `shared/utils/xthread_utils.py` and `shared/utils/thread_utils.py`) should avoid `time.sleep()` busy-waiting loops, as they continuously consume CPU cycles.
**Action:** Use `threading.Condition` with `wait()` and `notify()` to achieve zero idle CPU usage for asynchronous background task runners and message queues.
