import pytest
from datetime import datetime
from models.measurement import Measurement
from structures.measurement_buffer import MeasurementBuffer
from structures.measurement_queue import MeasurementQueue, EmptyQueueError
from structures.undo_stack import UndoStack, EmptyStackError

@pytest.fixture
def sample_measurements():
    """Testlerde kullanılacak örnek ölçüm verileri."""
    now = datetime.now()
    return [
        Measurement(
            measurement_id=f"M{i}", 
            sample_id="S1", 
            timestamp=now, 
            temperature=float(i * 10), 
            voltage=1.2  # <-- BURAYI EKLEDİK!
        )
        for i in range(1, 6) # M1:10.0, M2:20.0, M3:30.0, M4:40.0, M5:50.0
    ]


# --- BUFFER TESTLERİ ---

def test_buffer_invalid_max_size():
    """Sıfır veya negatif max_size durumunda ValueError fırlatılmalı."""
    with pytest.raises(ValueError):
        MeasurementBuffer(max_size=0)


def test_buffer_overflow_and_running_sum(sample_measurements):
    """
    Buffer dolduğunda eski elemanın otomatik düşmesi (Sliding Window)
    ve Running Sum'ın doğru hesaplanması testi.
    """
    buffer = MeasurementBuffer(max_size=3)
    
    # M1(10), M2(20), M3(30) ekleniyor. Toplam: 60, Ort: 20.0
    for m in sample_measurements[:3]:
        buffer.add(m)

    assert buffer.size() == 3
    assert buffer.average_temperature() == 20.0
    # Naive ile Running sum sonuçları aynı olmalı
    assert buffer.average_temperature() == buffer.average_temperature_naive()

    # M4(40) ekleniyor -> M1(10) düşmeli. Kalanlar: M2(20), M3(30), M4(40). Toplam: 90, Ort: 30.0
    buffer.add(sample_measurements[3])
    assert buffer.size() == 3
    assert buffer.latest().measurement_id == "M4"
    assert buffer.average_temperature() == 30.0


def test_buffer_encapsulation(sample_measurements):
    """values() metodunun dışarıya kopyasını verdiğini ve ana veriyi koruduğunu doğrular."""
    buffer = MeasurementBuffer(max_size=3)
    buffer.add(sample_measurements[0])
    
    vals = buffer.values()
    vals.clear() # Dışarıda temizliyoruz
    
    assert buffer.size() == 1 # İç kasanın bozulmadığını doğruluyoruz


# --- QUEUE (FIFO) TESTLERİ ---

def test_queue_fifo_behavior(sample_measurements):
    """Kuyruğun FIFO (İlk giren ilk çıkar) mantığını doğrular."""
    queue = MeasurementQueue()
    queue.enqueue(sample_measurements[0]) # M1
    queue.enqueue(sample_measurements[1]) # M2

    assert queue.peek().measurement_id == "M1"
    assert queue.dequeue().measurement_id == "M1"
    assert queue.dequeue().measurement_id == "M2"
    assert queue.is_empty() is True


def test_empty_queue_error():
    """Boş kuyruktan eleman çekilmeye çalışıldığında EmptyQueueError verilmeli."""
    queue = MeasurementQueue()
    with pytest.raises(EmptyQueueError):
        queue.dequeue()


# --- STACK (LIFO) TESTLERİ ---

def test_undo_stack_lifo_behavior():
    """Stack'in LIFO (Son giren ilk çıkar) mantığını doğrular."""
    stack = UndoStack()
    stack.push("İşlem 1")
    stack.push("İşlem 2")

    assert stack.pop() == "İşlem 2"
    assert stack.pop() == "İşlem 1"
    assert stack.is_empty() is True


def test_empty_stack_error():
    """Boş stack üzerinden pop yapıldığında EmptyStackError verilmeli."""
    stack = UndoStack()
    with pytest.raises(EmptyStackError):
        stack.pop()