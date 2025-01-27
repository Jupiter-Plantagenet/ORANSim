# oran/core/ru.py
import numpy as np
import scipy.constants as const

class RU:
    def __init__(self, carrier_frequency, num_antennas=1, max_tx_power_dbm=46):  # Default max power
        self.carrier_frequency = carrier_frequency  # Hz
        self.num_antennas = num_antennas
        self.max_tx_power_dbm = max_tx_power_dbm
        self.tx_power_dbm = self.max_tx_power_dbm  # Initialize to max
        self.tx_power_mw = 10**(self.tx_power_dbm / 10)
        self.noise_power = 0

    def set_tx_power(self, tx_power_dbm):
        if tx_power_dbm > self.max_tx_power_dbm:
            raise ValueError("Transmit power exceeds maximum allowed power")
        self.tx_power_dbm = tx_power_dbm
        self.tx_power_mw = 10**(self.tx_power_dbm / 10)

    def transmit(self, signal):
        if self.num_antennas > 1:
            if signal.ndim != 2 or signal.shape[0] != self.num_antennas:
                raise ValueError("Signal must be a 2D array (num_antennas, signal_length) for MIMO")
            transmitted_signal = signal * np.sqrt(self.tx_power_mw) / np.sqrt(self.num_antennas) #distribute power across antennas
        else:
            transmitted_signal = signal * np.sqrt(self.tx_power_mw)
        return transmitted_signal
    
    def add_awgn(self, signal, snr_db):
        signal_power_mw = np.mean(np.abs(signal)**2)
        signal_power_db = 10 * np.log10(signal_power_mw)
        noise_power_db = signal_power_db - snr_db
        self.noise_power = 10**(noise_power_db/10)
        noise = np.sqrt(self.noise_power/2) * (np.random.normal(0, 1, signal.shape) + 1j * np.random.normal(0, 1, signal.shape)) # AWGN
        noisy_signal = signal + noise
        return noisy_signal