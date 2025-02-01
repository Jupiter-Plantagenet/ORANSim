import yaml
from typing import Dict, Any, List, Optional
from pathlib import Path
import logging
from jsonschema import validate, ValidationError
import os
from enum import Enum

class ConfigStatus(Enum):
    """
    Enumerates configuration status values
    """
    APPLIED = "applied"
    ROLLED_BACK = "rolled_back"
    COMMITTED = "committed"

class O1Interface:
    """
    Simulates the O1 interface for network management using NETCONF/YANG emulation.

    This class reads configurations from YAML files, validates them against a schema, and provides methods for applying those configurations to network nodes.
    It also supports configuration versioning, rollback, and commit.
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
        self.config_history: Dict[str, List[Dict[str, Any]]] = {}  # For versioning
        self.config_status: Dict[str, Dict[str, Any]] = {} # For storing the status of nodes
        self._load_config_schema()
        self._load_configs()
        self.logger = logging.getLogger(self.__class__.__name__)

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
        """Loads and validates all configurations from YAML files in the config directory."""
        if not self.config_path.is_dir():
            raise FileNotFoundError(f"Config directory not found: {self.config_path}")

        for file_path in self.config_path.glob("*.yaml"):
            try:
                with open(file_path, "r") as file:
                    config = yaml.safe_load(file)
                    self._validate_config(config, file_path)
                    self._store_config(config)
            except ValidationError as e:
                self.logger.error(f"Validation error in file {file_path}: {e}")
            except Exception as e:
                self.logger.error(f"Error loading config from {file_path}: {e}")

    def _validate_config(self, config: Dict[str, Any], file_path: Path):
        """
        Validates the given config against the schema.

        Args:
            config (Dict[str, Any]): The configuration to validate.
            file_path (Path): Path to the configuration file (for logging purposes).
        """
        try:
            validate(instance=config, schema=self.config_schema)
        except ValidationError as e:
            self.logger.error(f"Configuration validation failed for file: {file_path}. Error: {e}")
            raise e

    def _store_config(self, config: Dict[str, Any]):
        """
        Stores the validated configuration in the node_configs dictionary and updates the history.

        Args:
            config (Dict[str, Any]): The validated configuration to store.
        """
        node_id = config["node_id"]

        # Store the current configuration
        if node_id not in self.node_configs:
          self.node_configs[node_id] = {}

        for key, value in config.items():
          self.node_configs[node_id][key] = value

        # Add config to history
        if node_id not in self.config_history:
          self.config_history[node_id] = []
        
        self.config_history[node_id].append(config)

        # Add a config status
        if node_id not in self.config_status:
          self.config_status[node_id] = {}
        self.config_status[node_id]["status"] = ConfigStatus.APPLIED
        self.config_status[node_id]["version"] = len(self.config_history[node_id]) - 1

    def get_node_config(self, node_id: str) -> Dict[str, Any]:
        """
        Returns the current node configuration for a specific node id.

        Args:
            node_id (str): The id of the node.
        Returns:
            Dict[str, Any]: The current configuration for the node.
        """
        if node_id not in self.node_configs:
            raise KeyError(f"Configuration not found for node id {node_id}")
        return self.node_configs[node_id]

    def apply_config(self, node, node_id: str):
        """
        Applies a configuration to a given node.

        Args:
            node: The node to apply the configuration to.
            node_id (str): The id of the node.
        """
        try:
            config = self.get_node_config(node_id)
            node.apply_o1_config(config)
            self.logger.info(f"Applied config to node {node_id} using O1 interface")
        except Exception as e:
            self.logger.error(f"Failed to apply config to node {node_id}: {e}")
    
    def apply_configs(self, nodes: Dict[str, Any]):
        """
        Applies configurations to multiple nodes.

        Args:
            nodes (Dict[str, Any]): A dictionary of nodes, keyed by node ID.
        """
        for node_id, node in nodes.items():
            try:
                self.apply_config(node, node_id)
            except Exception as e:
                self.logger.error(f"Failed to apply config to node {node_id}: {e}")

    def rollback_config(self, node_id: str, version: Optional[int] = None):
        """
        Rolls back the configuration of a node to a previous version.

        Args:
            node_id (str): The id of the node to rollback.
            version (int, optional): The version to rollback to. If None, rolls back to the previous version. Defaults to None.
        """
        if node_id not in self.config_history:
            raise KeyError(f"No configuration history found for node id {node_id}")

        history = self.config_history[node_id]

        if version is None:
            # Rollback to the previous version
            if len(history) > 1:
                version = len(history) - 2 # Get the second to last index
            else:
                raise ValueError(f"No previous configuration to rollback to for node id {node_id}")
        elif version < 0 or version >= len(history):
            raise ValueError(f"Invalid version number {version} for node id {node_id}")

        # Get the config to apply
        config_to_apply = self.config_history[node_id][version]

        # Update the current configuration
        self.node_configs[node_id] = config_to_apply

        # Add a config status
        if node_id not in self.config_status:
          self.config_status[node_id] = {}
        self.config_status[node_id]["status"] = ConfigStatus.ROLLED_BACK
        self.config_status[node_id]["version"] = version

        self.logger.info(f"Configuration for node {node_id} rolled back to version {version}")

    def commit_config(self, node_id: str):
        """
        Commits the current configuration of a node.

        Args:
            node_id (str): The id of the node to commit the configuration for.
        """
        if node_id not in self.config_status:
          raise Exception(f"Cannot commit configuration. No configuration found for node id {node_id}")

        self.config_status[node_id]["status"] = ConfigStatus.COMMITTED

        self.logger.info(f"Configuration for node {node_id} committed")

    def reload_configs(self):
      """Reloads the configurations from the configuration directory"""
      self._load_configs()