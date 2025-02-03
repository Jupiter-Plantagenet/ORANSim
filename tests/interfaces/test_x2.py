import pytest
from oransim.core.interfaces.x2 import X2Interface
from oransim.simulation.scheduler import ORANScheduler

# Mock nodes for testing
class MockNode:
    def __init__(self, node_id):
        self.node_id = node_id
        self.received_messages = []

    def receive_x2_message(self, message, source_node_id):
        self.received_messages.append((message, source_node_id))

# Mock Scheduler
class MockScheduler:
    def add_event(self, delay, callback, *args):
        callback(*args)

# Test Fixtures
@pytest.fixture
def scheduler():
    return MockScheduler()

@pytest.fixture
def x2_interface(scheduler):
    return X2Interface(scheduler)

@pytest.fixture
def node_a():
    return MockNode("node_a")

@pytest.fixture
def node_b():
    return MockNode("node_b")

# Test Cases
def test_x2_interface_initialization(x2_interface, scheduler):
    assert x2_interface.scheduler == scheduler
    assert x2_interface.nodes == {}

def test_x2_interface_register_node(x2_interface, node_a):
    x2_interface.register_node("node_a", node_a)
    assert "node_a" in x2_interface.nodes
    assert x2_interface.nodes["node_a"] == node_a

def test_x2_interface_register_node_already_registered(x2_interface, node_a, caplog):
    x2_interface.register_node("node_a", node_a)
    x2_interface.register_node("node_a", node_a)
    assert "already registered" in caplog.text

def test_x2_interface_unregister_node(x2_interface, node_a):
    x2_interface.register_node("node_a", node_a)
    x2_interface.unregister_node("node_a")
    assert "node_a" not in x2_interface.nodes

def test_x2_interface_unregister_node_not_found(x2_interface, caplog):
    x2_interface.unregister_node("node_a")
    assert "not found" in caplog.text

def test_x2_interface_send_message(x2_interface, node_a, node_b):
    x2_interface.register_node("node_a", node_a)
    x2_interface.register_node("node_b", node_b)
    message = {"key": "value"}
    x2_interface.send_message(message, "node_a", "node_b")
    assert len(node_b.received_messages) == 1
    assert node_b.received_messages[0] == (message, "node_a")

def test_x2_interface_send_message_source_not_registered(x2_interface, node_b):
    x2_interface.register_node("node_b", node_b)
    message = {"key": "value"}
    with pytest.raises(ValueError):
        x2_interface.send_message(message, "node_a", "node_b")

def test_x2_interface_send_message_destination_not_registered(x2_interface, node_a):
    x2_interface.register_node("node_a", node_a)
    message = {"key": "value"}
    with pytest.raises(ValueError):
        x2_interface.send_message(message, "node_a", "node_b")