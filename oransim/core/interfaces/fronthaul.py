from dataclasses import dataclass  
import numpy as np  

@dataclass  
class FronthaulConfig:  
    latency_mean: float = 0.1    # Seconds  
    latency_std: float = 0.02    # Jitter  
    compression_ratio: float = 1.0  # Simulate IQ compression  

class FronthaulInterface:  
    def __init__(self, config: FronthaulConfig):  
        self.config = config  
        self.connected_du = None  

    def connect_du(self, o_du):  
        """Bind this fronthaul to an O-DU"""  
        self.connected_du = o_du  

    def transmit_iq(self, iq_data: np.ndarray) -> Optional[np.ndarray]:  
        """Apply fronthaul effects (latency, compression) to IQ data"""  
        if self.config.compression_ratio < 1.0:  
            iq_data = self._compress_iq(iq_data)  
        return iq_data  

    def _compress_iq(self, iq_data: np.ndarray) -> np.ndarray:  
        """Simple IQ compression simulation (quantization noise)"""  
        scale = 127 * self.config.compression_ratio  
        return np.round(iq_data * scale) / scale  