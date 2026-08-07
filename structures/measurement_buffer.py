from collections import deque
from models.measurement import Measurement

class MeasurementBuffer:
    """
    Son N adet ölçümü sabit boyutlu bir tampon bellekte (buffer) tutan
    ve hareketli ortalamayi (running sum) O(1) sürede hesaplayan sinif.
    """

    def __init__(self, max_size: int):
        # Görev 3: max_size kontrolü (Invariant koruması)
        if max_size <= 0:
            raise ValueError("Buffer boyutu (max_size) sıfırdan büyük bir pozitif tam sayı olmalıdır!")

        self._max_size: int = max_size
        # Görev 4: deque(maxlen=max_size) ile son N ölçümü tutan yapı
        self._buffer: deque[Measurement] = deque(maxlen=max_size)
        # Görev 7: O(1) Running Sum için toplam değişkeni
        self._running_sum: float = 0.0

    def add(self, measurement: Measurement) -> None:
        """
        Buffer'a yeni ölçüm ekler.
        Limit dolduysa en eski eleman düşer ve running sum güncellenir.
        """
        # Eğer buffer tamamen doluysa, en eski elemanın sıcaklığını toplamdan çıkarıyoruz
        if len(self._buffer) == self._max_size:
            oldest_measurement = self._buffer[0]
            self._running_sum -= oldest_measurement.temperature  # .value yerine .temperature

        # Yeni ölçümü ekleyip sıcaklığını toplama dahil ediyoruz
        self._buffer.append(measurement)
        self._running_sum += measurement.temperature  

    def latest(self) -> Measurement | None:
        """En son eklenen ölçümü döndürür."""
        if not self._buffer:
            return None
        return self._buffer[-1]

    def size(self) -> int:
        """Mevcut ölçüm sayısını döndürür."""
        return len(self._buffer)

    def values(self) -> list[Measurement]:
        """
        Görev 5: Encapsulation sızıntısını önlemek için 
        iç koleksiyonun yüzeysel bir kopyasını döndürür.
        """
        return list(self._buffer)

    def average_temperature_naive(self) -> float:
        """
        Görev 6: Bütün pencereyi gezerek (O(N)) ortalama hesaplayan ilk yöntem.
        """
        if not self._buffer:
            return 0.0
        total = sum(m.temperature for m in self._buffer)
        return total / len(self._buffer)

    def average_temperature(self) -> float:
        """
        Görev 7: Running Sum kullanarak O(1) sürede ortalama hesaplayan optimize yöntem.
        """
        if not self._buffer:
            return 0.0
        return self._running_sum / len(self._buffer)