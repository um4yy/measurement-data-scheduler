from typing import List, Optional
from models.measurement import Measurement
from algorithms.searching import linear_search_by_id, binary_search_by_timestamp
from algorithms.sorting import python_sorted_by_temperature

def search_by_id(measurements: List[Measurement], target_id: str) -> Optional[Measurement]:
    """Sırasız veride ID ile arama yapar (Linear Search)."""
    return linear_search_by_id(measurements, target_id)

def search_by_timestamp(measurements: List[Measurement], target_timestamp: str) -> Optional[Measurement]:
    """
    Timestamp'e göre sıralanmış veri üzerinde binary search yapar.
    Ön koşul: measurements zaman damgasına göre sıralı olmalıdır!
    """
    return binary_search_by_timestamp(measurements, target_timestamp)

def get_sorted_by_temperature(measurements: List[Measurement]) -> List[Measurement]:
    """Sıcaklığa göre sıralanmış yeni bir liste döndürür."""
    return python_sorted_by_temperature(measurements)