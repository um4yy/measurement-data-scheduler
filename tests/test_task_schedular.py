import pytest
from models.experiment_task import ExperimentTask, TaskStatus
from structures.task_scheduler import TaskScheduler
from models.exceptions import EmptySchedulerError, DuplicateTaskError, TaskNotFoundError

def test_priority_order():
    """Öncelik değeri küçük olanın önce çıkmasını test eder (1 > 10)."""
    scheduler = TaskScheduler()
    t_low = ExperimentTask("T1", "S1", 10, "Düşük Öncelik")
    t_high = ExperimentTask("T2", "S2", 1, "Yüksek Öncelik")
    
    scheduler.add_task(t_low)
    scheduler.add_task(t_high)
    
    assert scheduler.get_next_task().task_id == "T2"
    assert scheduler.get_next_task().task_id == "T1"

def test_fifo_stability():
    """Aynı öncelikteki görevlerde eklenme sırasının (FIFO) korunduğunu test eder."""
    scheduler = TaskScheduler()
    t1 = ExperimentTask("T1", "S1", 5, "İlk Gelen")
    t2 = ExperimentTask("T2", "S2", 5, "İkinci Gelen")
    
    scheduler.add_task(t1)
    scheduler.add_task(t2)
    
    assert scheduler.get_next_task().task_id == "T1"
    assert scheduler.get_next_task().task_id == "T2"

def test_lazy_deletion():
    """İptal edilen görevin atlandığını doğrular."""
    scheduler = TaskScheduler()
    t1 = ExperimentTask("T1", "S1", 1, "İptal Edilecek")
    t2 = ExperimentTask("T2", "S2", 2, "Normal Görev")
    
    scheduler.add_task(t1)
    scheduler.add_task(t2)
    
    scheduler.cancel_task("T1")
    
    # T1 iptal edildiği için direkt T2 gelmeli
    assert scheduler.get_next_task().task_id == "T2"

def test_duplicate_task_error():
    """Aynı task_id eklendiğinde DuplicateTaskError fırlatılmasını test eder."""
    scheduler = TaskScheduler()
    t1 = ExperimentTask("T1", "S1", 1, "Görev 1")
    t2 = ExperimentTask("T1", "S1", 1, "Aynı ID'li Görev")
    
    scheduler.add_task(t1)
    with pytest.raises(DuplicateTaskError):
        scheduler.add_task(t2)

def test_empty_scheduler_error():
    """Boş kuyruktan görev istendiğinde EmptySchedulerError fırlatılmasını test eder."""
    scheduler = TaskScheduler()
    with pytest.raises(EmptySchedulerError):
        scheduler.get_next_task()