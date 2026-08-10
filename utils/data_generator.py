import random
from datetime import datetime, timedelta
from typing import List
from models.measurement import Measurement

def generate_deterministic_measurements(count: int, seed: int = 42) -> List[Measurement]:
    # Rastgelelik tohumunu sabitliyoruz, böylece her çalışmada aynı veri üretilir
    random.seed(seed)
    base_time = datetime(2026, 1, 1, 0, 0, 0)
    
    measurements = []
    for i in range(count):
        timestamp = (base_time + timedelta(seconds=i)).isoformat()
        measurement_id = f"M-{i}"
        temperature = round(random.uniform(15.0, 35.0), 2)
        sample_id = f"S-{i}"
        voltage = round(random.uniform(3.0, 5.0), 2)
        
        measurements.append(Measurement(
            measurement_id=measurement_id,
            timestamp=timestamp,
            temperature=temperature,
            sample_id=sample_id,
            voltage=voltage
        ))
        
    return measurements