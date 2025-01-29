import yaml
from typing import Dict, Any, List
from pathlib import Path
import logging
from jsonschema import validate, ValidationError
import os


class O1Interface:
    """
    Simulates the O1 interface for network management using NETCONF/YANG emulation.

    This class reads configurations from YAML files, validates them against a schema, and provides methods for applying those configurations to network nodes.
    """

    def __init__(self, config_path: str, config_schema_path: str):
        """
        Initializes the O1 Interface.

        Args:
            config_path (str): The path to the directory containing YAML configuration files.
            config_schema_path (str): Path to the JSON schema file for validation.
        """
        self.config_path = Path(config_path)
        self.config_schema_path = Path(config_schema_path)
        self.node_configs: Dict[str, Dict[str, Any]] = {}
        self._load_config_schema()
        self._load_configs()

    def _load_config_schema(self):
        """Loads the JSON schema for configuration validation."""
        if not self.config_schema_path.is_file():
            raise FileNotFoundError(f"Config schema not found: {self.config_schema_path}")
        try:
            with open(self.config_schema_path, "r") as f:
                self.config_schema = yaml.safe_load(f)
        except Exception as e:
            raise Exception(f"Could not load config schema {self.config_schema_path}. Exception: {e}")


    def _load_configs(self):
        """Loads all configurations from YAML files in the config directory, validates them and stores them."""
        if not self.config_path.is_dir():
            raise FileNotFoundError(f"Config directory not found: {self.config_path}")
        
        self.node_configs = {} # clear previous configs before loading

        for file_path in self.config_path.glob("*.yaml"):
            try:
                with open(file_path, "r") as file:
                  config = yaml.safe_load(file)
                  if config:
                    self._validate_config(config, file_path)
                    if "node_id" in config:
                      node_id = config["node_id"]
                      self.node_configs[node_id] = config
                    else:
                      logging.warning(f"Warning: Invalid config file {file_path}. Node ID missing. Skipping file...")
                  else:
                      logging.warning(f"Warning: Invalid config file {file_path}. Skipping file...")

            except Exception as e:
                logging.error(f"Warning: Could not load config file {file_path}. Exception: {e}")
                continue


    def _validate_config(self, config: Dict[str, Any], file_path: Path):
      """Validates the given config against the schema"""
      try:
          validate(instance=config, schema=self.config_schema)
      except ValidationError as e:
          logging.error(f"Configuration validation failed for file: {file_path}. Error: {e}")
          raise e

    def get_node_config(self, node_id: str) -> Dict[str, Any]:
        """
        Returns the node configuration for a specific node id.

        Args:
            node_id (str): The id of the node.
        Returns:
            Dict[str, Any]: The configuration for the node.
        """
        if node_id in self.node_configs:
          return self.node_configs[node_id]
        else:
            raise KeyError(f"Configuration not found for node id {node_id}")

    def apply_config(self, node, node_id: str):
        """
        Applies a configuration to a given node.

        Args:
          node: The node to apply the configuration to.
          node_id (str): The id of the node to apply the configuration to.
        """
        try:
          config = self.get_node_config(node_id)
          node.apply_o1_config(config)
        except Exception as e:
          logging.error(f"Could not apply config for node {node_id}. Exception: {e}")
    
    def reload_configs(self):
      """Reloads the configurations from the configuration directory"""
      self._load_configs()