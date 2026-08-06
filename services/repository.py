from models.measurement import Measurement
from models.exceptions import DuplicateMeasurementError

class MeasurementRepository:
    def __init__(self):
        # Kayıt sırasını korumak için list
        self._measurements_list: list[Measurement] = []   # _ ile kapsülleme (encapsulation) sağlanır, dışarıdan erişim engellenir.
        # ID üzerinden O(1) erişim sağlamak için dict
        self._measurements_dict: dict[str, Measurement] = {}

    def add(self, measurement: Measurement) -> None:
        # Tekrarlı ID kontrolü
        if measurement.measurement_id in self._measurements_dict:
            raise DuplicateMeasurementError(
                f"Measurement ID '{measurement.measurement_id}' zaten mevcut!"
            )
        
        # İki koleksiyona da ekliyoruz
        self._measurements_list.append(measurement)
        self._measurements_dict[measurement.measurement_id] = measurement

    def get_by_id(self, measurement_id: str) -> Measurement | None:
        """
        Adım 11: ID üzerinden O(1) zaman karmaşıklığı ile ölçüm getirir.
        Bulunamazsa None döner.
        """
        return self._measurements_dict.get(measurement_id)

    def get_all(self) -> list[Measurement]:
        """Adım 11: Ekleme sırası korunmuş tüm ölçümleri liste olarak döner."""
        return self._measurements_list.copy()

    def get_unique_sample_ids(self) -> set[str]:
        """
        Adım 10: Sistemdeki tüm benzersiz sample_id değerlerini set olarak döner.
        """
        return {m.sample_id for m in self._measurements_list}