import heapq
from typing import List, Dict, Optional, Tuple
from models.experiment_task import ExperimentTask, TaskStatus

# Özel hatalarımızı merkezi exceptions modülümüzden import ediyoruz!
from models.exceptions import EmptySchedulerError, DuplicateTaskError, TaskNotFoundError

class TaskScheduler:
    """
    Deney görevlerini öncelik sırasına göre yöneten Heap tabanlı planlayıcı.
    """
    
    def __init__(self):
        self._heap: List[Tuple[int, int, ExperimentTask]] = []
        self._sequence_counter: int = 0
        self._task_index: Dict[str, ExperimentTask] = {}

    def is_empty(self) -> bool:
        """Kuyrukta bekleyen aktif (PENDING) görev olup olmadığını kontrol eder."""
        return self.pending_count() == 0

    def pending_count(self) -> int:
        """Kuyrukta PENDING durumunda olan görevlerin sayısını döner."""
        return sum(1 for task in self._task_index.values() if task.status == TaskStatus.PENDING)

    def add_task(self, task: ExperimentTask) -> None:
        """Yeni bir görevi öncelik kuyruğuna ekler."""
        if task.task_id in self._task_index:
            raise DuplicateTaskError(f"'{task.task_id}' ID'li görev zaten mevcut!")

        # Heap Tuple Yapısı: (Priority, Sequence_Number, Task_Object)
        heap_item = (task.priority, self._sequence_counter, task)
        heapq.heappush(self._heap, heap_item)
        
        # Sayaç ve İndeks Güncelleme
        self._sequence_counter += 1
        self._task_index[task.task_id] = task

    def peek_next(self) -> ExperimentTask:
        """En yüksek öncelikli PENDING görevi kuyruktan SİLMEDEN gösterir."""
        self._purge_cancelled_from_top()  # Baştaki iptal edilmişleri temizle
        if not self._heap:
            raise EmptySchedulerError("Kuyrukta bekleyen görev yok!")
        return self._heap[0][2]

    def get_next_task(self) -> ExperimentTask:
        """En yüksek öncelikli PENDING görevi kuyruktan ÇIKARARAK döner."""
        while self._heap:
            priority, seq, task = heapq.heappop(self._heap)
            
            # Lazy Deletion Kontrolü: İptal edilmişse atla!
            if task.status == TaskStatus.CANCELLED:
                continue
                
            task.status = TaskStatus.COMPLETED  # İşleneceği için COMPLETED yapıyoruz
            return task
            
        raise EmptySchedulerError("Kuyrukta çalıştırılacak görev bulunamadı!")

    def cancel_task(self, task_id: str) -> None:
        """Verilen ID'li görevi iptal eder (Lazy Deletion)."""
        if task_id not in self._task_index:
            raise TaskNotFoundError(f"'{task_id}' ID'li görev bulunamadı!")
            
        task = self._task_index[task_id]
        if task.status == TaskStatus.PENDING:
            task.status = TaskStatus.CANCELLED

    def _purge_cancelled_from_top(self) -> None:
        """Yardımcı Metot: Heap'in en tepesindeki iptal edilmiş görevleri temizler."""
        while self._heap and self._heap[0][2].status == TaskStatus.CANCELLED:
            heapq.heappop(self._heap)