from models.measurement import Measurement
from models.exceptions import DuplicateMeasurementError
from services.repository import MeasurementRepository


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


if __name__ == "__main__":
    main()