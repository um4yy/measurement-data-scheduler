from models.measurement import Measurement
from models.exceptions import DuplicateMeasurementError
from services.repository import MeasurementRepository
# --- 4. Gün Importları ---
from models.experiment_task import ExperimentTask
from structures.task_scheduler import TaskScheduler
from models.exceptions import EmptySchedulerError


def run_day4_simulation():
    print("\n" + "="*40)
    print("=== DENEY ZAMANLAYICI (4. GÜN - HEAP SCHEDULER) ===")
    print("="*40 + "\n")

    scheduler = TaskScheduler()

    # Görevler oluşturuluyor (1: Acil, 5: Normal, 10: Düşük)
    t1 = ExperimentTask("TASK-001", "SMP-A1", 5, "Normal Sıcaklık Ölçümü - 1")
    t2 = ExperimentTask("TASK-002", "SMP-A2", 5, "Normal Sıcaklık Ölçümü - 2")
    t_urgent = ExperimentTask("TASK-999", "SMP-ALARM", 1, "GÜVENLİK ALARMI: Yüksek Voltaj")
    t_routine = ExperimentTask("TASK-003", "SMP-R1", 10, "Rutin Cihaz Kalibrasyonu")

    print("📥 Görevler kuyruğa ekleniyor...")
    scheduler.add_task(t1)        # Priority: 5 (İlk eklendi)
    scheduler.add_task(t2)        # Priority: 5 (İkinci eklendi - FIFO)
    scheduler.add_task(t_routine) # Priority: 10
    scheduler.add_task(t_urgent)  # Priority: 1 (Son eklendi ama EN ACİL!)

    print(f" Toplam Bekleyen Görev: {scheduler.pending_count()}\n")

    # Lazy Deletion Testi
    print("🚫 'TASK-002' görevi iptal ediliyor (Lazy Deletion)...")
    scheduler.cancel_task("TASK-002")
    print(f" İptal sonrası aktif bekleyen: {scheduler.pending_count()}\n")

    # Görevleri Öncelik Sırasına Göre Çalıştırma
    print("⚡ GÖREV İŞLEME AKIŞI:")
    while not scheduler.is_empty():
        task = scheduler.get_next_task()
        print(f"  -> [ÇALIŞTIRILDI] ID: {task.task_id} | Öncelik: {task.priority} | Açıklama: {task.description}")


def main():
    print("===  ÖLÇÜM VERİ SİSTEMİ (1. GÜN) ===\n")

    repo = MeasurementRepository()

    # Adım 12: En az 5 farklı ölçüm verisi tanımlıyoruz
    m1 = Measurement("M101", "SAMPLE_A", 1700000000.0, 24.5, 5.0)
    m2 = Measurement("M102", "SAMPLE_B", 1700000005.0, 25.1, 5.1)
    m3 = Measurement("M103", "SAMPLE_A", 1700000010.0, 24.8, 4.9)
    m4 = Measurement("M104", "SAMPLE_C", 1700000015.0, 26.3, 5.2)
    m5 = Measurement("M105", "SAMPLE_B", 1700000020.0, 25.0, 5.0)

    # Ölçümleri Depoya Ekleme
    print("📥 5 adet ölçüm depoya ekleniyor...")
    for m in [m1, m2, m3, m4, m5]:
        repo.add(m)
    print(" 5 ölçüm başarıyla eklendi.\n")

    # List Kullanımı: Kayıt Sırasını Gösterme
    print("📋 Tüm Ölçümler (Geliş/Ekleme Sırasıyla - List):")
    for item in repo.get_all():
        print(f"  - [{item.measurement_id}] Numune: {item.sample_id} | Temp: {item.temperature}°C | Volt: {item.voltage}V")

    # Dict Kullanımı: O(1) Hızlı Erişim
    print("\n ID ile Hızlı Erişim (O(1) - Dict):")
    target_id = "M103"
    found = repo.get_by_id(target_id)
    print(f"  ID '{target_id}' sorgulandı -> Bulunan Veri: {found}")

    # Set Kullanımı: Benzersiz Numune ID'leri
    print("\n Benzersiz Numune ID'leri (Set):")
    unique_samples = repo.get_unique_sample_ids()
    print(f"  Benzersiz Numune Kümesi: {unique_samples}")

    # Tekrarlı Kimlik Senaryosu (Duplicate ID Testi)
    print("\n Tekrarlı Kimlik (Duplicate ID) Senaryosu:")
    duplicate_m = Measurement("M101", "SAMPLE_D", 1700000025.0, 30.0, 5.5)  # M101 zaten var!
    try:
        print(f"  -> Mevcut ID ({duplicate_m.measurement_id}) ile yeni kayıt eklenmeye çalışılıyor...")
        repo.add(duplicate_m)
    except DuplicateMeasurementError as e:
        print(f"   Hata Yakalandı (Beklenen Davranış): {e}")

run_day4_simulation()

if __name__ == "__main__":
    main()