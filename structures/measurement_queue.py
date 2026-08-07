from collections import deque
from models.measurement import Measurement


class EmptyQueueError(Exception):
    """Kuyruk boşken eleman çekilmeye çalışıldığında fırlatılan özel hata sınıfı."""
    pass


class MeasurementQueue:
    """
    FIFO (İlk Giren İlk Çıkar) prensibiyle çalışan ölçüm kuyruğu.
    """

    def __init__(self):
        # İç yapıda performans için deque kullanıyoruz
        self._queue: deque[Measurement] = deque()

    def enqueue(self, measurement: Measurement) -> None:
        """Kuyruğun sonuna yeni ölçüm ekler (O(1))."""
        self._queue.append(measurement)

    def dequeue(self) -> Measurement:
        """Kuyruğun başındaki ölçümü çıkarır ve döndürür (O(1))."""
        if self.is_empty():
            raise EmptyQueueError("Boş kuyruk üzerinden dequeue işlemi yapılamaz!")
        return self._queue.popleft()

    def peek(self) -> Measurement:
        """Kuyruğun başındaki ölçümü çıkarmadan sadece görüntüler (O(1))."""
        if self.is_empty():
            raise EmptyQueueError("Boş kuyruk üzerinde peek işlemi yapılamaz!")
        return self._queue[0]

    def is_empty(self) -> bool:
        """Kuyruğun boş olup olmadığını kontrol eder."""
        return len(self._queue) == 0

    def size(self) -> int:
        """Kuyruktaki toplam eleman sayısını döndürür."""
        return len(self._queue)