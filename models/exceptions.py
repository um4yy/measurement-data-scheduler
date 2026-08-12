class DuplicateMeasurementError(Exception):
    """Ayni measurement_id ile tekrar kayit eklenmek istendiğinde firlatilir."""
    pass

class BaseProjectError(Exception):
    """Projedeki tüm özel hataların türediği ata sınıf."""
    pass

class EmptySchedulerError(BaseProjectError):
    """Boş kuyruktan görev çekilmeye veya bakılmaya çalışıldığında fırlatılır."""
    pass

class DuplicateTaskError(BaseProjectError):
    """Aynı task_id ile ikinci kez görev eklenmeye çalışıldığında fırlatılır."""
    pass

class TaskNotFoundError(BaseProjectError):
    """İptal edilmek istenen task_id bulunamadığında fırlatılır."""
    pass