import time

class Timer:
    def __init__(self, duration):
        self.duration = duration
    
    def __enter__(self):
        self.start_time = time.time()
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.end_time = time.time()
        self.elapsed = self.end_time - self.start_time
        if self.elapsed > self.duration:
            raise TimeoutError(f"Operation exceeded the time limit of {self.duration} seconds")
        if exc_type is not None:
            # Re-raise the exception if any exception was caught
            return False

    def has_time_left(self):
        return time.time() - self.start_time < self.duration