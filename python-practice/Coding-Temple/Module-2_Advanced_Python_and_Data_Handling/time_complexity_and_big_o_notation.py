#Write two different functions that both count how many pairs of numbers in a list sum to a given target. One should be O(n²) (nested loops), the other should be O(n) (using a set or dictionary). Benchmark both on lists of size 1,000, 5,000, and 10,000 using the timing pattern from the Guided Example.

#O(n²) (nested loops)
def count_pairs_slow(data, target): 
    count = 0 
    for i in range(len(data)): 
        for j in range(i + 1, len(data)):
            if data[i] + data[j] == target: 
                count += 1
    return count

#O(n) (using a set or dictionary)
def count_pairs_fast(data, target):
    seen = set()
    count = 0 
    for item in data: 
        complement = target - item 
        if complement in seen: 
            count += 1
        seen.add(item)
    return count

#Benchmarking
import time 
import random

def benchmark(func, data, target): 
    start = time.time()
    result = func(data, target)
    end = time.time()
    return end - start

# Generate test data with no duplicates (worst case -- must check everything)
sizes = [1000, 5000, 10000]

for size in sizes:
    data = list(range(size))        # No duplicates -- forces full scan
    random.shuffle(data)            # Randomize order
    target = len(data) // 2
    t1 = benchmark(count_pairs_slow, data, target)
    t2 = benchmark(count_pairs_fast, data, target)
    print(f"n={size:>6}  |  Slow: {t1:.4f}s  |  Fast: {t2:.4f}s")





