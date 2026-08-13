import bisect
from typing import List, Optional
from models.measurement import Measurement
from models.experiment_task import ExperimentTask
from services.repository import MeasurementRepository
from structures.measurement_buffer import MeasurementBuffer
from structures.task_scheduler import TaskScheduler

class ExperimentManager:
    """
    Tüm alt sistemleri (Repository, Buffer, Scheduler) orkestre eden ana yönetim sınıfı.
    Composition ve Dependency Injection prensiplerini kullanır.
    """
    def __init__(
        self, 
        repository: MeasurementRepository, 
        buffer: MeasurementBuffer, 
        scheduler: TaskScheduler
    ):
        # ADIM 2 & 3: Dependency Injection (Sınıflar dışarıdan enjekte edilir)
        self.repository = repository
        self.buffer = buffer
        self.scheduler = scheduler

    # ADIM 4: Görev Yönetimi
    def submit_task(self, task: ExperimentTask) -> None:
        """Yeni görevi zamanlayıcıya delege eder."""
        self.scheduler.add_task(task)

    def process_next_task(self) -> Optional[ExperimentTask]:
        """Zamanlayıcıdaki en acil görevi çeker."""
        return self.scheduler.get_next_task()

    # ADIM 6 & 7: Tek Kontrollü Atomik Akış (Veri Tutarlılığı Koruması)
    def add_measurement(self, measurement: Measurement) -> None:
        """
        Ölçümü hem repository hem buffer'a ekler.
        Eğer tekrarlayan ID (Duplicate) hatası çıkarsa Buffer'ın tutarsız kalmasını engeller.
        """
        # 1. Önce Repository'ye ekle (Hata varsa burada fırlatılır, işlem durur)
        self.repository.add(measurement)
        
        # 2. Hata çıkmadıysa Buffer'a güvenle ekle
        self.buffer.add(measurement)

    # ADIM 8: O(1) Dictionary Index Araması
    def get_measurement_by_id(self, measurement_id: str) -> Optional[Measurement]:
        return self.repository.get_by_id(measurement_id)

    # ADIM 9: Timestamp ile Binary Search (O(log N))
    def find_measurements_by_time_range(self, start_time: float, end_time: float) -> List[Measurement]:
        all_measurements = self.repository.get_all()
        timestamps = [m.timestamp for m in all_measurements]
        
        left_idx = bisect.bisect_left(timestamps, start_time)
        right_idx = bisect.bisect_right(timestamps, end_time)
        
        return all_measurements[left_idx:right_idx]

    # ADIM 10: Sistem Özeti 
    def get_system_summary(self) -> dict:
        recent_measurements = self.buffer.get_last_n(self.buffer.capacity)
        avg_temp = 0.0
        if recent_measurements:
            avg_temp = sum(m.temperature for m in recent_measurements) / len(recent_measurements)

        return {
            "total_measurements": len(self.repository.get_all()),
            "unique_samples_count": len(self.repository.get_unique_sample_ids()),
            "pending_tasks_count": self.scheduler.pending_count(),
            "recent_window_avg_temp": round(avg_temp, 2)
        }