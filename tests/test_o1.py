import pytest
import numpy as np
from oransim.core.nodes import O_RU, RUConfig, O_DU, BaseStationConfig
from oransim.core.interfaces.o1 import O1Interface
from oransim.simulation.scheduler import ORANScheduler
from oransim.core.interfaces.e2 import E2Termination
import tempfile
import os
import yaml
from jsonschema import ValidationError

def create_temp_config_dir():
  """Creates a temporary directory with a sample config file."""
  temp_dir = tempfile.mkdtemp()
  config_file_path = os.path.join(temp_dir, "config1.yaml")
  config_data = {
      "node_id": "o_ru_1",
      "frequency": 3.6e9,
      "bandwidth": 120e6,
      "tx_power": 47.0
  }
  
  with open(config_file_path, "w") as f:
    yaml.dump(config_data, f)
  
  config_file_path_2 = os.path.join(temp_dir, "config2.yaml")
  config_data_2 = {
        "node_id": "o_du_1",
        "max_ues": 150,
        "transmit_power": 47.0
    }
  with open(config_file_path_2, "w") as f:
      yaml.dump(config_data_2, f)

  config_file_path_3 = os.path.join(temp_dir, "config3.yaml")
  config_data_3 = {
      "node_id": "o_ru_2",
      "frequency": 3.7e9,
      "bandwidth": 110e6,
        "tx_power": 48.0
  }
  with open(config_file_path_3, "w") as f:
      yaml.dump(config_data_3, f)


  config_file_path_invalid = os.path.join(temp_dir, "config_invalid.yaml")
  config_data_invalid = {
    "frequency": 3.8e9,
    "bandwidth": 120e6,
        "tx_power": 49.0
  }

  with open(config_file_path_invalid, "w") as f:
    yaml.dump(config_data_invalid, f)



  return temp_dir


def test_o1_interface():
    temp_config_dir = create_temp_config_dir()
    
    o1_interface = O1Interface(config_path=temp_config_dir, config_schema_path="config_schema.yaml")
    scheduler = ORANScheduler()
    e2_term = E2Termination()

    ru_config = RUConfig(ru_id=1)
    o_ru = O_RU(ru_config, scheduler)

    ru_config_2 = RUConfig(ru_id=2)
    o_ru_2 = O_RU(ru_config_2, scheduler)

    du_config = BaseStationConfig(cell_id=101)
    o_du = O_DU(du_config, scheduler) # Removed e2_term here


    # Apply the config
    o1_interface.apply_config(o_ru, "o_ru_1")
    o1_interface.apply_config(o_ru_2, "o_ru_2")
    o1_interface.apply_config(o_du, "o_du_1")

    assert o_ru.config.frequency == 3.6e9
    assert o_ru.config.bandwidth == 120e6
    assert o_ru.config.tx_power == 47.0

    assert o_ru_2.config.frequency == 3.7e9
    assert o_ru_2.config.bandwidth == 110e6
    assert o_ru_2.config.tx_power == 48.0
    
    assert o_du.config.max_ues == 150
    assert o_du.config.transmit_power == 47.0

    # Check that an invalid configuration cannot be loaded
    with pytest.raises(KeyError):
        o1_interface.get_node_config("invalid_config")
    
    # Check dynamic reloading of configuration files
    config_file_path_new = os.path.join(temp_config_dir, "config2.yaml")
    config_data_new = {
      "node_id": "o_du_1",
      "max_ues": 200,
      "transmit_power": 48.0
      }
    with open(config_file_path_new, "w") as f:
        yaml.dump(config_data_new, f)
    
    o1_interface.reload_configs()
    o1_interface.apply_config(o_du, "o_du_1")

    assert o_du.config.max_ues == 200
    assert o_du.config.transmit_power == 48.0

    os.system(f"rmdir /S /Q {temp_config_dir}")