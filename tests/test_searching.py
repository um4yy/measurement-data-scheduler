# tests/test_searching.py
import pytest
from models.measurement import Measurement
from algorithms.searching import linear_search_by_id, binary_search_by_timestamp

@pytest.fixture
def sample_measurements():
    """Testlerde kullanılacak sıralı örnek veri kümesi"""
    return [
        Measurement(
            measurement_id="M1", 
            timestamp="2026-08-10T10:00:00", 
            temperature=20.0,
            sample_id="S1",
            voltage=5.0
        ),
        Measurement(
            measurement_id="M2", 
            timestamp="2026-08-10T11:00:00", 
            temperature=22.5,
            sample_id="S2",
            voltage=5.1
        ),
        Measurement(
            measurement_id="M3", 
            timestamp="2026-08-10T12:00:00", 
            temperature=25.0,
            sample_id="S3",
            voltage=5.2
        ),
    ]

# --- LINEAR SEARCH TESTLERİ ---

def test_linear_search_found(sample_measurements):
    result = linear_search_by_id(sample_measurements, "M2")
    assert result is not None
    assert result.measurement_id == "M2"

def test_linear_search_not_found(sample_measurements):
    result = linear_search_by_id(sample_measurements, "M99")
    assert result is None

def test_linear_search_empty_list():
    result = linear_search_by_id([], "M1")
    assert result is None

# --- BINARY SEARCH TESTLERİ (Sınır Durumları) ---

def test_binary_search_first_element(sample_measurements):
    result = binary_search_by_timestamp(sample_measurements, "2026-08-10T10:00:00")
    assert result is not None
    assert result.measurement_id == "M1"

def test_binary_search_last_element(sample_measurements):
    result = binary_search_by_timestamp(sample_measurements, "2026-08-10T12:00:00")
    assert result is not None
    assert result.measurement_id == "M3"

def test_binary_search_single_element():
    single_item = [
        Measurement(
            measurement_id="M1", 
            timestamp="2026-08-10T10:00:00", 
            temperature=20.0,
            sample_id="S1",
            voltage=5.0
        )
    ]
    
    found = binary_search_by_timestamp(single_item, "2026-08-10T10:00:00")
    assert found is not None
    assert found.measurement_id == "M1"

    not_found = binary_search_by_timestamp(single_item, "2026-08-10T15:00:00")
    assert not_found is None

def test_binary_search_empty_list():
    result = binary_search_by_timestamp([], "2026-08-10T10:00:00")
    assert result is None