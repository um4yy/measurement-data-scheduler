from dataclasses import dataclass

@dataclass(frozen=True)    #Sınıfı salt okunur (immutable) yapar.
class Measurement:
    measurement_id: str
    sample_id: str
    timestamp: float
    temperature: float
    voltage: float