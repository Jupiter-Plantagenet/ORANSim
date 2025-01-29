import pytest  
import numpy as np  
from oransim.core.nodes import O_RU, RUConfig, O_DU, BaseStationConfig  
from oransim.simulation.scheduler import ORANScheduler  

class TestFronthaul:  
    def test_iq_transmission(self):  
        scheduler = ORANScheduler()  
        ru_config = RUConfig(ru_id=1)  
        du_config = BaseStationConfig(cell_id=101)  
        o_ru = O_RU(ru_config, scheduler)  
        o_du = O_DU(du_config, scheduler)  

        # Simulate IQ transmission from O-RU to O-DU  
        o_ru.send_iq_data(o_du)  
        scheduler.run(until=0.15)  # Run past 100ms latency  

        assert len(o_du.received_iq) == 1  
        assert isinstance(o_du.received_iq[0], np.ndarray)  