"""
The `data_models` subpackage contains Pydantic data models for representing 
various data structures used in the ORANSim library, such as:

- Messages exchanged over the ORAN interfaces (e.g., E2AP, E2SM, A1).
- Policies used for network management (e.g., A1 policies).
- Other relevant data structures.

Using Pydantic models provides several benefits, including:

- **Data Validation:** Pydantic automatically validates the data against the defined schema, 
  ensuring type safety and data integrity.
- **Serialization and Deserialization:** Pydantic makes it easy to serialize and deserialize 
  data to and from different formats like JSON.
- **Documentation:** Pydantic models serve as documentation for the data structures, 
  making it easier to understand the expected format and types.

Each data model is typically defined in its own module within this subpackage 
(e.g., `a1_policy.py`, `e2sm_kpm.py`).
"""

# This __init__.py file can be kept relatively simple. 
# Its main purpose is to mark the 'data_models' directory as a Python package.

# You can optionally import specific data models here to make them directly 
# accessible from the oransim.data_models package, e.g.:
# from oransim.data_models.a1_policy import A1Policy
# from oransim.data_models.e2sm_kpm import E2SM_KPM_IndicationMessage