import time
import random

total_time = 0
for _ in range(10000):
    start = time.perf_counter()
    sorted_data = sorted([random.uniform(0, 10000) for _ in range(10000)])
    end = time.perf_counter()
    total_time += (end - start)

print(f"Average sort time: {total_time / 10000:.6f} seconds")
print(f"Total sort time: {total_time:.6f} seconds")