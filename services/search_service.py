from typing import List, Optional
from models.measurement import Measurement
from algorithms.searching import linear_search_by_id, binary_search_by_timestamp
from algorithms.sorting import python_sorted_by_temperature

class MeasurementSearchService:
    def __init__(self, measurements: List[Measurement]):
        # Servis başlatılırken veri kümesini alıyoruz
        self._measurements = measurements

    def search_by_id(self, target_id: str) -> Optional[Measurement]:
        """Sırasız veride ID ile arama yapar (Linear Search)."""
        return linear_search_by_id(self._measurements, target_id)

    def search_by_timestamp(self, target_timestamp: str) -> Optional[Measurement]:
        """
        Timestamp'e göre sıralanmış veri üzerinde binary search yapar.
        Ön koşul: self._measurements zaman damgasına göre sıralı olmalıdır!
        """
        return binary_search_by_timestamp(self._measurements, target_timestamp)

    def get_sorted_by_temperature(self) -> List[Measurement]:
        """Sıcaklığa göre sıralanmış yeni bir liste döndürür."""
        return python_sorted_by_temperature(self._measurements)