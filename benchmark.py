import time
from utils.data_generator import generate_deterministic_measurements
from algorithms.searching import linear_search_by_id, binary_search_by_timestamp
from algorithms.sorting import python_sorted_by_temperature
from services.repository import MeasurementRepository  # 5. Gün için eklendi

def run_benchmark():
    sizes = [100, 10_000, 100_000]
    iterations = 50  # Tek ölçüme güvenmeyip ortalama alıyoruz

    # Tablo başlığı genişletildi: Dict Index O(1) sütunu eklendi
    print(f"{'Boyut (N)':<10} | {'Linear Search (s)':<18} | {'Binary Search (s)':<18} | {'Dict Index O(1) (s)':<20} | {'Sıralama (Sorted) (s)':<20}")
    print("-" * 95)

    for size in sizes:
        data = generate_deterministic_measurements(size)
        
        # 5. Gün Adım 11 için Repository indekslemesi
        repo = MeasurementRepository()
        for m in data:
            repo.add(m)

        # En kötü senaryo (Worst-Case): Aranan eleman listenin en sonunda!
        target_timestamp = data[-1].timestamp
        target_id = data[-1].measurement_id

        # 1. Linear Search Ölçümü - O(N)
        start = time.perf_counter()
        for _ in range(iterations):
            linear_search_by_id(data, target_id)
        linear_time = (time.perf_counter() - start) / iterations

        # 2. Binary Search Ölçümü - O(log N)
        start = time.perf_counter()
        for _ in range(iterations):
            binary_search_by_timestamp(data, target_timestamp)
        binary_time = (time.perf_counter() - start) / iterations

        # 3. Dict Index Ölçümü - O(1) (5. GÜN EKLENTİSİ)
        start = time.perf_counter()
        for _ in range(iterations):
            repo.get_by_id(target_id)
        dict_time = (time.perf_counter() - start) / iterations

        # 4. Sıralama Maliyeti Ölçümü
        start = time.perf_counter()
        python_sorted_by_temperature(data)
        sort_time = time.perf_counter() - start

        # Hepsi aynı hizada ekrana yazdırılıyor
        print(f"{size:<10} | {linear_time:<18.8f} | {binary_time:<18.8f} | {dict_time:<20.8f} | {sort_time:<20.8f}")

if __name__ == "__main__":
    run_benchmark()