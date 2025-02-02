import pytest
from oransim.interfaces.a1 import A1Interface, A1Policy, A1PolicyType
from oransim.core.ric import NonRTRIC, NearRTRIC
from jsonschema import ValidationError

# Mock NearRTRIC and NonRTRIC for testing
class MockNearRTRIC:
    def __init__(self, near_rt_ric_id: str):
        self.near_rt_ric_id = near_rt_ric_id
        self.received_policies = []
        self.logger = logging.getLogger(self.__class__.__name__)

    def store_a1_policy(self, policy):
        self.received_policies.append(policy)

class MockNonRTRIC:
    def __init__(self):
        self.sent_policies = []
        self.logger = logging.getLogger(self.__class__.__name__)

    def create_a1_policy(self, policy_type: A1PolicyType, policy_content: Dict[str, Any], target: str):
        policy_id = f"policy-{len(self.sent_policies) + 1}"
        return A1Policy(policy_type=policy_type, policy_id=policy_id, policy_content=policy_content, target=target)

    def send_a1_policy(self, policy, near_rt_ric):
        self.sent_policies.append((policy, near_rt_ric))

class MockScheduler:
    def add_event(self, delay, callback, *args):
        callback(*args)

# Test data
@pytest.fixture
def near_rt_ric():
    return MockNearRTRIC("near_rt_ric_1")

@pytest.fixture
def non_rt_ric():
    return MockNonRTRIC()

@pytest.fixture
def a1_interface(non_rt_ric, near_rt_ric):
    return A1Interface(non_rt_ric, near_rt_ric)

@pytest.fixture
def sample_policy_content():
    return {"threshold": 50, "action": "increase_power"}

@pytest.fixture
def sample_policy(sample_policy_content):
    return A1Policy(
        policy_type=A1PolicyType.TYPE_1,
        policy_id="test_policy_1",
        policy_content=sample_policy_content,
        target="o_du"
    )

# Test cases
def test_a1_interface_initialization(non_rt_ric, near_rt_ric):
    a1_interface = A1Interface(non_rt_ric, near_rt_ric)
    assert a1_interface.non_rt_ric == non_rt_ric
    assert a1_interface.near_rt_ric == near_rt_ric

def test_send_policy_valid(a1_interface, near_rt_ric, sample_policy):
    a1_interface.send_policy(sample_policy, near_rt_ric)
    assert len(near_rt_ric.received_policies) == 1
    assert near_rt_ric.received_policies[0] == sample_policy

def test_send_policy_invalid_near_rt_ric(a1_interface, sample_policy):
    with pytest.raises(ValueError):
        a1_interface.send_policy(sample_policy, MockNearRTRIC("another_near_rt_ric"))

def test_receive_policy_valid(a1_interface, near_rt_ric, sample_policy):
    result = a1_interface.receive_policy(sample_policy.model_dump())
    assert result is True
    assert len(near_rt_ric.received_policies) == 1
    assert near_rt_ric.received_policies[0] == sample_policy

def test_receive_policy_invalid_data(a1_interface, near_rt_ric):
    invalid_policy = {"invalid": "data"}
    result = a1_interface.receive_policy(invalid_policy)
    assert result is False
    assert len(near_rt_ric.received_policies) == 0