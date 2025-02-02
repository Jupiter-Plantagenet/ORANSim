import pytest
import numpy as np
from oransim.core.nodes import O_RU, O_DU, O_CU_CP, O_CU_UP, UE, RUConfig, DUConfig, CUCPConfig, CUUPConfig
from oransim.core.mobility import MobilityModel, RandomWalkModel
from oransim.simulation.scheduler import ORANScheduler

# Mock the scheduler for testing
class MockScheduler:
    def add_event(self, delay, callback, *args):
        pass
scheduler = MockScheduler()

# Test Data
@pytest.fixture
def sample_ru_config():
    return RUConfig(ru_id="ru_1", frequency=2.4e9, bandwidth=20e6, tx_power=30)

@pytest.fixture
def sample_du_config():
    return DUConfig(du_id="du_1", max_ues=10)

@pytest.fixture
def sample_cucp_config():
    return CUCPConfig(cucp_id="cucp_1")

@pytest.fixture
def sample_cuup_config():
    return CUUPConfig(cuup_id="cuup_1")

@pytest.fixture
def sample_mobility_model():
    return RandomWalkModel()

# Test Cases
def test_o_ru_initialization(sample_ru_config):
    o_ru = O_RU(sample_ru_config, scheduler)
    assert o_ru.config == sample_ru_config
    assert o_ru.scheduler == scheduler
    assert o_ru.connected_ues == set()
    assert o_ru.iq_buffer == []

def test_o_ru_generate_iq_data(sample_ru_config):
    o_ru = O_RU(sample_ru_config, scheduler)
    iq_data = o_ru.generate_iq_data()
    assert isinstance(iq_data, np.ndarray)

def test_o_du_initialization(sample_du_config):
    o_du = O_DU(sample_du_config, scheduler)
    assert o_du.config == sample_du_config
    assert o_du.scheduler == scheduler
    assert o_du.received_iq == []
    assert o_du.connected_ues == []

def test_o_cu_cp_initialization(sample_cucp_config):
    o_cu_cp = O_CU_CP(sample_cucp_config, scheduler)
    assert o_cu_cp.config == sample_cucp_config
    assert o_cu_cp.scheduler == scheduler

def test_o_cu_up_initialization(sample_cuup_config):
    o_cu_up = O_CU_UP(sample_cuup_config, scheduler)
    assert o_cu_up.config == sample_cuup_config
    assert o_cu_up.scheduler == scheduler

def test_ue_initialization(sample_mobility_model):
    initial_position = np.array([0, 0])
    ue = UE("ue_1", initial_position, sample_mobility_model, scheduler)
    assert ue.ue_id == "ue_1"
    assert np.array_equal(ue.position, initial_position)
    assert ue.mobility_model == sample_mobility_model
    assert ue.scheduler == scheduler
    assert ue.o_du is None

def test_ue_attach_detach(sample_du_config, sample_mobility_model):
    initial_position = np.array([0, 0])
    ue = UE("ue_1", initial_position, sample_mobility_model, scheduler)
    o_du = O_DU(sample_du_config, scheduler)

    ue.attach_to_du(o_du)
    assert ue.o_du == o_du
    assert ue in o_du.connected_ues

    ue.detach_from_du()
    assert ue.o_du is None
    assert ue not in o_du.connected_ues

# Add more test cases to cover other methods and functionalities of the node classes