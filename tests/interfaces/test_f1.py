import pytest
from oransim.core.interfaces.f1 import F1Interface
from oransim.simulation.scheduler import ORANScheduler

# Mock O-CU-CP, O-CU-UP, and O-DU classes for testing
class Mock_O_CU_CP:
    def __init__(self, cucp_id):
        self.cucp_id = cucp_id
        self.received_messages = []

    def receive_f1_message(self, message, source_node):
        self.received_messages.append((message, source_node))

class Mock_O_CU_UP:
    def __init__(self, cuup_id):
        self.cuup_id = cuup_id
        self.received_messages = []

    def receive_f1_message(self, message, source_node):
        self.received_messages.append((message, source_node))

class Mock_O_DU:
    def __init__(self, du_id):
        self.du_id = du_id
        self.received_messages = []

    def receive_f1_message(self, message, source_node):
        self.received_messages.append((message, source_node))

# Mock Scheduler
class MockScheduler:
    def add_event(self, delay, callback, *args):
        callback(*args)

# Test Fixtures
@pytest.fixture
def scheduler():
    return MockScheduler()

@pytest.fixture
def f1_interface(scheduler):
    return F1Interface(scheduler)

@pytest.fixture
def o_cu_cp():
    return Mock_O_CU_CP("cucp_1")

@pytest.fixture
def o_cu_up():
    return Mock_O_CU_UP("cuup_1")

@pytest.fixture
def o_du():
    return Mock_O_DU("du_1")

# Test Cases
def test_f1_interface_initialization(f1_interface, scheduler):
    assert f1_interface.scheduler == scheduler
    assert f1_interface.cu_up is None
    assert f1_interface.cu_cp is None
    assert f1_interface.du is None

def test_f1_interface_set_nodes(f1_interface, o_cu_cp, o_cu_up, o_du):
    f1_interface.set_cu_cp(o_cu_cp)
    f1_interface.set_cu_up(o_cu_up)
    f1_interface.set_du(o_du)

    assert f1_interface.cu_cp == o_cu_cp
    assert f1_interface.cu_up == o_cu_up
    assert f1_interface.du == o_du

def test_f1_interface_send_message_valid(f1_interface, o_cu_cp, o_cu_up, o_du):
    f1_interface.set_cu_cp(o_cu_cp)
    f1_interface.set_cu_up(o_cu_up)
    f1_interface.set_du(o_du)

    message = {"type": "TEST", "content": "Test message"}

    f1_interface.send_message(message, "o_du", "o_cu_cp")
    assert len(o_cu_cp.received_messages) == 1
    assert o_cu_cp.received_messages[0] == (message, "o_du")

    f1_interface.send_message(message, "o_du", "o_cu_up")
    assert len(o_cu_up.received_messages) == 1
    assert o_cu_up.received_messages[0] == (message, "o_du")

    f1_interface.send_message(message, "o_cu_cp", "o_du")
    assert len(o_du.received_messages) == 1
    assert o_du.received_messages[0] == (message, "o_cu_cp")

    f1_interface.send_message(message, "o_cu_up", "o_du")
    assert len(o_du.received_messages) == 2
    assert o_du.received_messages[1] == (message, "o_cu_up")

def test_f1_interface_send_message_invalid_source(f1_interface):
    message = {"type": "TEST", "content": "Test message"}
    with pytest.raises(ValueError):
        f1_interface.send_message(message, "invalid_source", "o_du")

def test_f1_interface_send_message_invalid_destination(f1_interface):
    message = {"type": "TEST", "content": "Test message"}
    with pytest.raises(ValueError):
        f1_interface.send_message(message, "o_du", "invalid_destination")

def test_f1_interface_send_message_destination_not_set(f1_interface, o_du):
    message = {"type": "TEST", "content": "Test message"}
    f1_interface.send_message(message, "o_du", "o_cu_cp")
    f1_interface.send_message(message, "o_du", "o_cu_up")
    # Ensure that no messages were received by the unset nodes
    assert len(o_du.received_messages) == 0