import pytest
from services.experiment_manager import ExperimentManager
from services.repository import MeasurementRepository
from structures.measurement_buffer import MeasurementBuffer
from structures.task_scheduler import TaskScheduler
from services.measurement_provider import RandomMeasurementProvider
from models.measurement import Measurement
from models.experiment_task import ExperimentTask
from models.exceptions import DuplicateMeasurementError

def test_experiment_manager_integration():
    """Bütün parçaların birlikte uyumlu çalıştığını doğrular."""
    repo = MeasurementRepository()
    buffer = MeasurementBuffer(max_size=5)
    scheduler = TaskScheduler()
    provider = RandomMeasurementProvider()

    manager = ExperimentManager(repository=repo, buffer=buffer, scheduler=scheduler)

    # Ölçüm ekleme testi
    m1 = provider.generate_measurement()
    manager.add_measurement(m1)

    assert manager.get_measurement_by_id(m1.measurement_id) == m1
    # Buffer elemanlarını almak için senin tanımladığın values() metodunu kullanıyoruz
    assert len(manager.buffer.values()) == 1

    # Task Scheduler testi
    task = ExperimentTask("T-001", m1.sample_id, 1, "Sıcaklık Alarmı")
    manager.submit_task(task)

    executed_task = manager.process_next_task()
    assert executed_task.task_id == "T-001"

def test_duplicate_measurement_rollback_and_consistency():
    """Duplicate ID durumunda Buffer tutarlılığının korunduğunu doğrular."""
    repo = MeasurementRepository()
    buffer = MeasurementBuffer(max_size=5)
    scheduler = TaskScheduler()

    manager = ExperimentManager(repo, buffer, scheduler)

    m1 = Measurement("M101", "SMP-1", 1000.0, 25.0, 5.0)
    m1_duplicate = Measurement("M101", "SMP-2", 1005.0, 30.0, 5.5)

    manager.add_measurement(m1)
    assert len(buffer.values()) == 1

    # İkinci aynı ID'li veride hata fırlatılmalı ve Buffer etkilenmemeli
    with pytest.raises(DuplicateMeasurementError):
        manager.add_measurement(m1_duplicate)

    # TUTARLILIK KONTROLÜ: Hatalı eleman Buffer'a girmemiş olmalı
    assert len(buffer.values()) == 1