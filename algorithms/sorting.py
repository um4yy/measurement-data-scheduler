def insertion_sort_by_temperature(measurements: List[Measurement]) -> List[Measurement]:
    # Orijinal listeyi bozmamak için kopyasını alıyoruz (Side-effect önleme)
    arr = list(measurements)
    
    for i in range(1, len(arr)):
        key_item = arr[i]
        j = i - 1
        # Sıcaklık değerine göre geriye doğru kaydırma işlemi
        while j >= 0 and arr[j].temperature > key_item.temperature:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key_item
        
    return arr

def python_sorted_by_temperature(measurements: List[Measurement]) -> List[Measurement]:
    return sorted(measurements, key=lambda m: m.temperature)