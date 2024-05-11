import time
import multiprocessing

def factorize_sync(number):
    factors = []
    for i in range(1, number + 1):
        if number % i == 0:
            factors.append(i)
    return factors

def factorize_multi(number):
    factors = []
    with multiprocessing.Pool() as pool:
        for i in range(1, number + 1):
            if number % i == 0:
                factors.append(i)
    return factors

def measure_time(func, *args):
    start_time = time.time()
    result = func(*args)
    end_time = time.time()
    return result, end_time - start_time

if __name__ == "__main__":
    numbers = [128, 255, 99999, 10651060]

    for num in numbers:
        print(f"Number: {num}")
        result_sync, time_sync = measure_time(factorize_sync, num)
        print(f"Synchronous: {result_sync}, Time: {time_sync}")

        result_multi, time_multi = measure_time(factorize_multi, num)
        print(f"Multiprocessing: {result_multi}, Time: {time_multi}")

        print()
