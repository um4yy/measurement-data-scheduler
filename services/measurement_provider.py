import time
import random
from models.measurement import Measurement

class RandomMeasurementProvider:
    """
    Test ve simülasyonlar için rastgele ölçüm üreten örnek provider.
    Gerçek senaryoda bu bir dosya okuyucu veya sensör sürücüsü olabilir.
    """
    def __init__(self, sample_prefix="SMP"):
        self.sample_prefix = sample_prefix
        self._counter = 100

    def generate_measurement(self) -> Measurement:
        self._counter += 1
        m_id = f"M{self._counter}"
        s_id = f"{self.sample_prefix}_{random.randint(1, 5)}"
        return Measurement(
            measurement_id=m_id,
            sample_id=s_id,
            timestamp=time.time(),
            temperature=round(random.uniform(20.0, 30.0), 2),
            voltage=round(random.uniform(4.5, 5.5), 2)
        )