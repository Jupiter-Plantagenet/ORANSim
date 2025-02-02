import yaml
import logging
from typing import Dict, Any, Union, List
from pathlib import Path
from jsonschema import validate, ValidationError

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def load_config(config_path: Union[str, Path], schema_path: Union[str, Path] = None) -> Dict[str, Any]:
    """
    Loads and parses a YAML configuration file.

    Args:
        config_path (Union[str, Path]): The path to the YAML configuration file.
        schema_path (Union[str, Path], optional): The path to the JSON schema file for validation. 
                                                  If None, no validation is performed. Defaults to None.

    Returns:
        Dict[str, Any]: The parsed configuration data as a dictionary.

    Raises:
        FileNotFoundError: If the config file or schema file does not exist.
        yaml.YAMLError: If there is an error parsing the YAML file.
        ValidationError: If the configuration data is invalid according to the schema.
        Exception: If any other error occurs.
    """
    config_path = Path(config_path)
    if not config_path.is_file():
        raise FileNotFoundError(f"Configuration file not found: {config_path}")

    if schema_path:
        schema_path = Path(schema_path)
        if not schema_path.is_file():
            raise FileNotFoundError(f"Schema file not found: {schema_path}")

    try:
        with open(config_path, "r") as f:
            config_data = yaml.safe_load(f)
    except yaml.YAMLError as e:
        raise yaml.YAMLError(f"Error parsing YAML file {config_path}: {e}")

    if schema_path:
        try:
            with open(schema_path, "r") as f:
                schema = yaml.safe_load(f)
        except Exception as e:
            raise Exception(f"Error loading schema from {schema_path}: {e}")
        
        try:
            validate(instance=config_data, schema=schema)
        except ValidationError as e:
            raise ValidationError(f"Configuration validation failed for file: {config_path}. Error: {e}")

    logging.info(f"Configuration file loaded successfully: {config_path}")
    return config_data

# Example usage (you can add this to your main simulation script or a separate config loading module):
# try:
#     config = load_config("config.yaml", "config_schema.yaml")
#     print(config)
# except Exception as e:
#     logging.error(f"Error loading configuration: {e}")