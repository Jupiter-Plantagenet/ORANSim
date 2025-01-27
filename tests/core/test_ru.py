# tests/core/test_ru.py
import pytest
import numpy as np
from oran.core.ru import RU

def test_ru_transmit_single_antenna():
    ru = RU(2.6e9, 40)
    signal = np.array([1, 2, 3])
    transmitted_signal = ru.transmit(signal)
    assert np.all(transmitted_signal >= 0)

def test_ru_transmit_mimo():
    ru = RU(2.6e9, 40, num_antennas=2)
    signal = np.array([[1, 2, 3], [4, 5, 6]])
    transmitted_signal = ru.transmit(signal)
    assert transmitted_signal.shape == signal.shape
    assert np.all(transmitted_signal >= 0)

def test_add_awgn():
    ru = RU(2.6e9, 40)
    signal = np.array([1, 2, 3])
    snr_db = 10
    noisy_signal = ru.add_awgn(signal, snr_db)
    assert noisy_signal.shape == signal.shape

def test_ru_transmit_mimo_incorrect_signal_shape():
    ru = RU(2.6e9, 40, num_antennas=2)
    signal = np.array([1, 2, 3])  # Incorrect shape
    with pytest.raises(ValueError):
        ru.transmit(signal)

def test_set_tx_power():
    ru = RU(2.6e9, 46) # Initialize with max power
    ru.set_tx_power(40)
    assert ru.tx_power_dbm == 40
    assert ru.tx_power_mw == 10**(40/10)

def test_set_tx_power_exceeds_max():
    ru = RU(2.6e9, 46)
    with pytest.raises(ValueError):
        ru.set_tx_power(50)