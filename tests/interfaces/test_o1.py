import pytest
import os
import yaml
from oransim.interfaces.o1 import O1Interface, ConfigStatus
from oransim.core.nodes import O_RU, O_DU, RUConfig, DUConfig
from oransim.simulation.scheduler import ORANScheduler
from jsonschema import ValidationError
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Mock the scheduler for testing
class MockScheduler:
    def add_event(self, delay, callback, *args):
        pass

# Mock node classes for testing
class MockNode:
    def __init__(self, node_id):
        self.node_id = node_id
        self.config = {}

    def apply_o1_config(self, config):
        self.config.update(config)

@pytest.fixture
def scheduler():
    return MockScheduler()

@pytest.fixture
def o1_config_path(tmpdir):
    # Create a temporary directory for config files
    config_dir = tmpdir.mkdir("config")

    # Create a sample config file for an O-RU
    o_ru_config_data = {
        "node_id": "o_ru_1",
        "frequency": 3.6e9,
        "bandwidth": 100e6,
        "tx_power": 30,
        "supported_operations": ["start", "stop", "reconfigure"],
        "cells": [{"cell_id": "cell_1", "max_ues": 50}, {"cell_id": "cell_2", "max_ues": 75}],
    }
    o_ru_config_file = config_dir.join("o_ru_config.yaml")
    with open(o_ru_config_file, "w") as f:
        yaml.dump(o_ru_config_data, f)

    # Create a sample config file for an O-DU
    o_du_config_data = {
        "node_id": "o_du_1",
        "max_ues": 100,
        "schedulers": ["scheduler_1", "scheduler_2"],
        "cells": [{"cell_id": "cell_3", "du_id": "du_1", "max_ues": 60}],
    }
    o_du_config_file = config_dir.join("o_du_config.yaml")
    with open(o_du_config_file, "w") as f:
        yaml.dump(o_du_config_data, f)

    # Create an invalid config file (missing node_id)
    invalid_config_data = {
        "frequency": 3.8e9,
        "bandwidth": 20e6,
    }
    invalid_config_file = config_dir.join("invalid_config.yaml")
    with open(invalid_config_file, "w") as f:
        yaml.dump(invalid_config_data, f)

    return str(config_dir)

@pytest.fixture
def config_schema_path(tmpdir):
    # Create a sample JSON schema for O1 configuration
    schema = {
        "type": "object",
        "required": ["node_id"],
        "properties": {
            "node_id": {"type": "string"},
            "frequency": {"type": "number"},
            "bandwidth": {"type": "number"},
            "tx_power": {"type": "number"},
            "max_ues": {"type": "integer"},
            "cells": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "cell_id": {"type": "string"},
                        "du_id": {"type": "string"},
                        "max_ues": {"type": "integer"},
                    },
                },
            },
            "schedulers": {
                "type": "array",
                "items": {"type": "string"},
            },
            "supported_operations": {
                "type": "array",
                "items": {"type": "string"},
            },
        },
    }

    schema_file = tmpdir.join("config_schema.yaml")
    with open(schema_file, "w") as f:
        yaml.dump(schema, f)

    return str(schema_file)

@pytest.fixture
def o1_interface(o1_config_path, config_schema_path):
    return O1Interface(config_path=o1_config_path, config_schema_path=config_schema_path)

def test_o1_interface_load_valid_configs(o1_interface):
    assert "o_ru_1" in o1_interface.node_configs
    assert "o_du_1" in o1_interface.node_configs

    assert o1_interface.node_configs["o_ru_1"]["node_id"] == "o_ru_1"
    assert o1_interface.node_configs["o_ru_1"]["frequency"] == 3.6e9

    assert o1_interface.node_configs["o_du_1"]["node_id"] == "o_du_1"
    assert o1_interface.node_configs["o_du_1"]["max_ues"] == 100

def test_o1_interface_load_invalid_config_file(o1_interface, caplog):
    with pytest.raises(ValidationError):
        o1_interface.get_node_config("invalid_config")
    assert "Configuration validation failed" in caplog.text

def test_o1_interface_apply_config(o1_interface, scheduler):
    o_ru_config = RUConfig(ru_id="o_ru_1")
    o_ru = O_RU(o_ru_config, scheduler)
    o1_interface.apply_config(o_ru, "o_ru_1")
    assert o_ru.config.frequency == 3.6e9

    o_du_config = DUConfig(du_id="o_du_1")
    o_du = O_DU(o_du_config, scheduler)
    o1_interface.apply_config(o_du, "o_du_1")
    assert o_du.config.max_ues == 100

def test_o1_interface_apply_configs(o1_interface, scheduler):
    o_ru_config = RUConfig(ru_id="o_ru_1")
    o_ru = O_RU(o_ru_config, scheduler)
    du_config = DUConfig(du_id="o_du_1")
    o_du = O_DU(du_config, scheduler)
    nodes = {"o_ru_1": o_ru, "o_du_1": o_du}

    o1_interface.apply_configs(nodes)

    assert o_ru.config.frequency == 3.6e9
    assert o_du.config.max_ues == 100

def test_o1_interface_get_node_config(o1_interface):
    config = o1_interface.get_node_config("o_ru_1")
    assert config["node_id"] == "o_ru_1"
    assert config["frequency"] == 3.6e9

    with pytest.raises(KeyError):
        o1_interface.get_node_config("nonexistent_node")

def test_o1_interface_rollback_config(o1_interface, scheduler):
    o_ru_config = RUConfig(ru_id="o_ru_1")
    o_ru = O_RU(o_ru_config, scheduler)
    o1_interface.apply_config(o_ru, "o_ru_1")

    # Modify config directly to simulate a change
    o1_interface.node_configs["o_ru_1"]["frequency"] = 3.8e9
    o1_interface.config_history["o_ru_1"].append({"node_id": "o_ru_1", "frequency": 3.8e9})
    o1_interface.config_status["o_ru_1"]["version"] = 1

    o1_interface.rollback_config("o_ru_1", 0)
    assert o1_interface.get_node_config("o_ru_1")["frequency"] == 3.6e9
    assert o1_interface.config_status["o_ru_1"]["status"] == ConfigStatus.ROLLED_BACK

def test_o1_interface_commit_config(o1_interface, scheduler):
    o_ru_config = RUConfig(ru_id="o_ru_1")
    o_ru = O_RU(o_ru_config, scheduler)
    o1_interface.apply_config(o_ru, "o_ru_1")

    o1_interface.commit_config("o_ru_1")
    assert o1_interface.config_status["o_ru_1"]["status"] == ConfigStatus.COMMITTED

def test_o1_interface_reload_configs(o1_interface, o1_config_path):
    # Modify a configuration file
    config_file_path = os.path.join(o1_config_path, "o_du_config.yaml")
    with open(config_file_path, "w") as f:
        config_data = {
            "node_id": "o_du_1",
            "max_ues": 200,
            "schedulers": ["scheduler_1"],
            "cells": [{"cell_id": "cell_3", "du_id": "du_1", "max_ues": 100}],
        }
        yaml.dump(config_data, f)

    o1_interface.reload_configs()
    config = o1_interface.get_node_config("o_du_1")
    assert config["max_ues"] == 200