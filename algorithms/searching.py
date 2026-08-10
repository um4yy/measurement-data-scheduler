from typing import List, Optional
from models.measurement import Measurement

def linear_search_by_id(measurements: List[Measurement], target_id: str) -> Optional[Measurement]:
    for item in measurements:
        if item.measurement_id == target_id:
            return item
    return None

def binary_search_by_timestamp(measurements: List[Measurement], target_timestamp: str) -> Optional[Measurement]:
    low = 0
    high = len(measurements) - 1

    while low <= high:
        mid = (low + high) // 2
        current_time = measurements[mid].timestamp

        if current_time == target_timestamp:
            return measurements[mid]
        elif current_time < target_timestamp:
            low = mid + 1  # Aradığımız zaman daha ileride, sol yarıyı eliyoruz
        else:
            high = mid - 1 # Aradığımız zaman daha geride, sağ yarıyı eliyoruz

    return None