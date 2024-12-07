import time

class Stopwatch:
    def __enter__(self):
        self.start = time.time()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.end = time.time()
        self.elapsed = self.end - self.start
    
    def get_elapsed(self):
        return round(self.elapsed, 1)

# Usage example
if __name__ == '__main__':
    with Stopwatch() as sw:
        # Some code to time
        for _ in range(5):
            time.sleep(1)
            
    print(f'Elapsed time: {sw.get_elapsed()}s')
    