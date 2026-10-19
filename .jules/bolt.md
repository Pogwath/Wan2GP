## 2024-10-19 - Eliminate Thread Busy Waiting
**Learning:** Background thread polling mechanisms like `Listener` and `FIFOQueue` in `shared/utils/xthread_utils.py` and `shared/utils/thread_utils.py` were using `time.sleep(0.001)` busy-waiting loops.
**Action:** Use `threading.Condition` with `wait()` and `notify()` to achieve zero idle CPU usage for background tasks instead of polling with `time.sleep`.
