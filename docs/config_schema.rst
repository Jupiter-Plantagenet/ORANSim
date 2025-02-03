.. _config_schema:

Configuration Schema
====================

ORANSim uses YAML files for configuration. This document describes the 
schema for the configuration files.

The following parameters are supported:

.. list-table::
   :header-rows: 1

   * - Parameter
     - Type
     - Description
     - Default Value
   * - `simulation.duration`
     - Number
     - The duration of the simulation in seconds.
     - `1000`
   * - `simulation.random_seed`
     - Integer
     - The random seed for the simulation.
     - `42`
   # Add more parameters and their descriptions here

Example Configuration File
--------------------------

.. code-block:: yaml

   simulation:
     duration: 1000
     random_seed: 42

   # ... other configuration parameters