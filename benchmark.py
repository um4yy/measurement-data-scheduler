import time
from utils.data_generator import generate_deterministic_measurements
from algorithms.searching import linear_search_by_id, binary_search_by_timestamp
from algorithms.sorting import python_sorted_by_temperature

def run_benchmark():
    sizes = [100, 10_000, 100_000]
    iterations = 50  # Tek ölçüme güvenmeyip ortalama alıyoruz

    print(f"{'Boyut (N)':<10} | {'Linear Search (s)':<20} | {'Binary Search (s)':<20} | {'Sıralama (Sorted) (s)':<20}")
    print("-" * 80)

    for size in sizes:
        data = generate_deterministic_measurements(size)
        # En kötü senaryo (Worst-Case): Aranan eleman listenin en sonunda!
        target_timestamp = data[-1].timestamp
        target_id = data[-1].measurement_id

        # 1. Linear Search Ölçümü
        start = time.perf_counter()
        for _ in range(iterations):
            linear_search_by_id(data, target_id)
        linear_time = (time.perf_counter() - start) / iterations

        # 2. Binary Search Ölçümü
        start = time.perf_counter()
        for _ in range(iterations):
            binary_search_by_timestamp(data, target_timestamp)
        binary_time = (time.perf_counter() - start) / iterations

        # 3. Sıralama Maliyeti Ölçümü (Adım 11)
        start = time.perf_counter()
        python_sorted_by_temperature(data)
        sort_time = time.perf_counter() - start

        print(f"{size:<10} | {linear_time:<20.8f} | {binary_time:<20.8f} | {sort_time:<20.8f}")

if __name__ == "__main__":
    run_benchmark()