from services.experiment_manager import ExperimentManager
from services.repository import MeasurementRepository
from structures.measurement_buffer import MeasurementBuffer
from structures.task_scheduler import TaskScheduler
from services.measurement_provider import RandomMeasurementProvider
from models.experiment_task import ExperimentTask
from models.exceptions import DuplicateMeasurementError

def run_final_demo():
    print("=" * 60)
    print(" MEASUREMENT DATA SCHEDULER & EXPERIMENT MANAGER - FINAL DEMO")
    print("=" * 60 + "\n")

    # 1. Dependency Injection ile Alt Sistemlerin Başlatılması (Composition)
    repo = MeasurementRepository()
    buffer = MeasurementBuffer(max_size=5)
    scheduler = TaskScheduler()
    provider = RandomMeasurementProvider()

    manager = ExperimentManager(repository=repo, buffer=buffer, scheduler=scheduler)
    print(" ExperimentManager ve tüm alt sistemler (DI / Composition) başarıyla yüklendi.")

    # 2. Ölçüm Verisi Ekleme Akışı
    print("\n Rastgele Ölçüm Verileri Eklendi:")
    for _ in range(3):
        m = provider.generate_measurement()
        manager.add_measurement(m)
        print(f"  -> Ölçüm Eklendi | ID: {m.measurement_id} | Sıcaklık: {m.temperature}°C | Numune: {m.sample_id}")

    # 3. Sistem Özeti Çıktısı
    summary = manager.get_system_summary()
    print(f"\n Sistem Genel Özeti: {summary}")

    # 4. Task Scheduler (Öncelikli Görev / Max-Heap) Kullanımı
    print("\nDeney Görevleri Zamanlayıcıya Ekleniyor...")
    task_routine = ExperimentTask("TASK-101", "SMP-A1", priority=5, description="Rutin Sıcaklık Ölçümü")
    task_urgent = ExperimentTask("TASK-999", "SMP-ALARM", priority=1, description="GÜVENLİK ALARMI: Yüksek Voltaj")

    manager.submit_task(task_routine)
    manager.submit_task(task_urgent)
    print(f"  -> Toplam Bekleyen Görev Sayısı: {scheduler.pending_count()}")

    print("\n Öncelikli Görev Çalıştırılıyor (1: En Acil):")
    executed_task = manager.process_next_task()
    print(f"  -> İşlenen Görev: ID: {executed_task.task_id} | Öncelik: {executed_task.priority} | Açıklama: '{executed_task.description}'")

    print("\n" + "=" * 60)
    print(" FINAL DEMO BAŞARIYLA TAMAMLANDI")
    print("=" * 60 + "\n")

if __name__ == "__main__":
    run_final_demo()