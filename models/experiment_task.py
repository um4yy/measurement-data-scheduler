from enum import Enum
from dataclasses import dataclass

# 1. Görev Durumlarını Belirleyen Enum Sınıfı
class TaskStatus(Enum):
    PENDING = "PENDING"      # Görev oluşturuldu, kuyrukta bekliyor
    COMPLETED = "COMPLETED"  # Görev başarıyla çalıştırıldı ve bitti
    CANCELLED = "CANCELLED"  # Görev çalıştırılmadan iptal edildi


# 2. Deney Görevi Veri Modeli (Dataclass)
@dataclass
class ExperimentTask:
    task_id: str          # Görevin benzersiz kimliği (Örn: "TASK-101")
    sample_id: str        # Ölçüm yapılacak numunenin ID'si (Örn: "SMP-005")
    priority: int         # Görevin aciliyeti (1: En yüksek acil, 10: Düşük öncelik)
    description: str      # Görevin ne yaptığına dair açıklama
    status: TaskStatus = TaskStatus.PENDING  # Varsayılan durum: PENDING