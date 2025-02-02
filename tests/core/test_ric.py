import pytest
from oransim.core.ric import NearRTRIC, NonRTRIC
from oransim.core.interfaces.a1 import A1Interface, A1Policy, A1PolicyType
from oransim.core.interfaces.e2 import E2Interface
from oransim.core.nodes import O_DU, DUConfig

# Mock the scheduler, A1, and E2 interfaces for testing
class MockScheduler:
    def add_event(self, delay, callback, *args):
        pass

class MockA1Interface:
    def send_policy(self, policy, near_rt_ric):
        pass

class MockE2Interface:
    def send_indication(self, message, du_id):
        pass
    def subscribe(self, subscriber_id, callback):
        pass

# Test Data
@pytest.fixture
def scheduler():
    return MockScheduler()

@pytest.fixture
def a1_interface():
    return MockA1Interface()

@pytest.fixture
def e2_interface():
    return MockE2Interface()

@pytest.fixture
def sample_du_config():
    return DUConfig(du_id="du_1", max_ues=10)

@pytest.fixture
def sample_policy():
    return A1Policy(policy_type=A1PolicyType.TYPE_1, policy_id="policy_1", policy_content={"param1": "value1"}, target="o_du")

# Test Cases for NearRTRIC
def test_near_rt_ric_initialization(a1_interface, e2_interface, scheduler):
    near_rt_ric = NearRTRIC("near_rt_ric_1", a1_interface, e2_interface, scheduler)
    assert near_rt_ric.a1_interface == a1_interface
    assert near_rt_ric.e2_interface == e2_interface
    assert near_rt_ric.scheduler == scheduler
    assert near_rt_ric.xapps == {}
    assert near_rt_ric.a1_policies == {}
    assert near_rt_ric.e2_nodes == {}

def test_near_rt_ric_add_remove_xapp(a1_interface, e2_interface, scheduler):
    near_rt_ric = NearRTRIC("near_rt_ric_1", a1_interface, e2_interface, scheduler)

    class MockXApp:
        def __init__(self, xapp_id):
            self.xapp_id = xapp_id

        def receive_indication(self, message, du_id):
            pass

    xapp = MockXApp("xapp_1")
    near_rt_ric.add_xapp(xapp)
    assert "xapp_1" in near_rt_ric.xapps

    near_rt_ric.remove_xapp("xapp_1")
    assert "xapp_1" not in near_rt_ric.xapps

def test_near_rt_ric_receive_a1_policy(a1_interface, e2_interface, scheduler, sample_policy):
    near_rt_ric = NearRTRIC("near_rt_ric_1", a1_interface, e2_interface, scheduler)
    near_rt_ric.receive_a1_policy(sample_policy.model_dump())
    assert sample_policy.policy_id in near_rt_ric.a1_policies

def test_near_rt_ric_register_e2_node(a1_interface, e2_interface, scheduler, sample_du_config):
    near_rt_ric = NearRTRIC("near_rt_ric_1", a1_interface, e2_interface, scheduler)
    o_du = O_DU(sample_du_config, scheduler)
    near_rt_ric.register_e2_node("du_1", o_du)
    assert "du_1" in near_rt_ric.e2_nodes
    assert near_rt_ric.e2_nodes["du_1"] == o_du

# Test Cases for NonRTRIC
def test_non_rt_ric_initialization(a1_interface, scheduler):
    non_rt_ric = NonRTRIC(a1_interface, scheduler)
    assert non_rt_ric.a1_interface == a1_interface
    assert non_rt_ric.scheduler == scheduler
    assert non_rt_ric.rapps == {}
    assert non_rt_ric.managed_near_rt_rics == []

def test_non_rt_ric_add_remove_rapp(a1_interface, scheduler):
    non_rt_ric = NonRTRIC(a1_interface, scheduler)

    class MockRApp:
        def __init__(self, rapp_id):
            self.rapp_id = rapp_id

    rapp = MockRApp("rapp_1")
    non_rt_ric.add_rapp(rapp)
    assert "rapp_1" in non_rt_ric.rapps

    non_rt_ric.remove_rapp("rapp_1")
    assert "rapp_1" not in non_rt_ric.rapps

def test_non_rt_ric_create_a1_policy(a1_interface, scheduler):
    non_rt_ric = NonRTRIC(a1_interface, scheduler)
    policy = non_rt_ric.create_a1_policy(A1PolicyType.TYPE_1, {"param1": "value1"}, "o_du")
    assert isinstance(policy, A1Policy)
    assert policy.policy_type == A1PolicyType.TYPE_1

def test_non_rt_ric_send_a1_policy(a1_interface, e2_interface, scheduler, sample_policy):
    non_rt_ric = NonRTRIC(a1_interface, scheduler)
    near_rt_ric = NearRTRIC("near_rt_ric_1", a1_interface, e2_interface, scheduler)
    non_rt_ric.send_a1_policy(sample_policy, near_rt_ric)

def test_non_rt_ric_add_managed_near_rt_ric(a1_interface, e2_interface, scheduler):
    non_rt_ric = NonRTRIC(a1_interface, scheduler)
    near_rt_ric = NearRTRIC("near_rt_ric_1", a1_interface, e2_interface, scheduler)
    non_rt_ric.add_managed_near_rt_ric(near_rt_ric)
    assert near_rt_ric in non_rt_ric.managed_near_rt_rics

# Add more test cases to cover other methods and functionalities of NearRTRIC and NonRTRIC