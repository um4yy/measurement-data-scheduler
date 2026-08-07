from dataclasses import FrozenInstanceError
import pytest
from models.exceptions import DuplicateMeasurementError
from models.measurement import Measurement
from services.repository import MeasurementRepository


def test_measurement_immutability():
  """Measurement nesnesinin immutable (frozen) olduğunu doğrular."""
  m = Measurement('M1', 'S1', 1700000000.0, 25.5, 5.0)
  with pytest.raises(FrozenInstanceError):
    m.temperature = 30.0


def test_add_and_get_by_id():
  """Başarili ekleme ve ID ile O(1) erişimi test eder."""
  repo = MeasurementRepository()
  m1 = Measurement('M1', 'S1', 1700000000.0, 25.5, 5.0)
  repo.add(m1)

  retrieved = repo.get_by_id('M1')
  assert retrieved == m1
  assert retrieved.temperature == 25.5


def test_duplicate_measurement_error():
  """Ayni ID ikinci kez eklendiğinde DuplicateMeasurementError firlatildigini doğrular."""
  repo = MeasurementRepository()
  m1 = Measurement('M1', 'S1', 1700000000.0, 25.5, 5.0)
  m2 = Measurement('M1', 'S2', 1700000005.0, 26.0, 5.1)

  repo.add(m1)
  with pytest.raises(DuplicateMeasurementError):
    repo.add(m2)


def test_get_unique_sample_ids():
  """Set yapisinin benzersiz sample_id toplandiğini doğrular."""
  repo = MeasurementRepository()
  repo.add(Measurement('M1', 'SAMPLE_A', 1700000000.0, 25.5, 5.0))
  repo.add(Measurement('M2', 'SAMPLE_B', 1700000001.0, 26.0, 5.1))
  repo.add(Measurement('M3', 'SAMPLE_A', 1700000002.0, 25.8, 5.0))

  unique_samples = repo.get_unique_sample_ids()
  assert unique_samples == {'SAMPLE_A', 'SAMPLE_B'}
  assert len(unique_samples) == 2