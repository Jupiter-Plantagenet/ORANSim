.. _user_manual:

User Manual
===========

This user manual provides a comprehensive guide to using the ORANSim library for 
simulating 5G Open Radio Access Networks (ORAN). It covers the following topics:

- Installation
- Getting Started
- Configuration
- Running Simulations
- Key Components
- Extending ORANSim
- Troubleshooting
- FAQ

Installation
------------

ORANSim can be installed using pip:

.. code-block:: bash

   pip install oransim

Alternatively, you can clone the repository from GitHub and install it manually:

.. code-block:: bash

   git clone https://github.com/Jupiter-Plantagenet/ORANSim.git
   cd ORANSim
   pip install .

Getting Started
---------------

To get started with ORANSim, you need to create a configuration file that defines 
the simulation parameters, network topology, and other settings. A sample 
configuration file (`config.yaml`) is provided in the `examples` directory.

Here's a minimal example to run a simulation:

.. code-block:: python

   from oransim.simulation.scheduler import ORANScheduler
   from oransim.utils.config_loader import load_config

   # Load the configuration
   config = load_config("config.yaml")

   # Create a scheduler
   scheduler = ORANScheduler()

   # TODO: Add code here to create network nodes, interfaces, UEs, etc. based on the configuration

   # Run the simulation
   scheduler.run(until=config["simulation"]["duration"])

Configuration
-------------

ORANSim uses YAML files for configuration. The configuration file allows you to 
specify various parameters for the simulation, including:

- Network topology (number and types of nodes)
- Node configurations (e.g., frequency, bandwidth, power)
- Mobility models
- Traffic models
- xApp/rApp configurations
- Data collection settings

A detailed description of the configuration schema can be found in :ref:`config_schema`.

Running Simulations
-------------------

To run a simulation, you need to:

1. Create a configuration file.
2. Write a Python script that:
    - Loads the configuration using `oransim.utils.config_loader.load_config`.
    - Creates an instance of `oransim.simulation.scheduler.ORANScheduler`.
    - Creates instances of network nodes, UEs, and interfaces based on the configuration.
    - Adds the UEs to the scheduler.
    - Calls the `run()` method of the scheduler to start the simulation.

Key Components
--------------

.. toctree::
   :maxdepth: 1

   key_components/nodes
   key_components/ric
   key_components/interfaces
   key_components/mobility
   key_components/xapp_rapp

Extending ORANSim
-----------------

ORANSim is designed to be extensible. You can add new functionalities by:

- Creating new mobility models that inherit from `oransim.core.mobility.MobilityModel`.
- Implementing new xApps and rApps by inheriting from `oransim.xapp_rapp_framework.xapp.XApp` and `oransim.xapp_rapp_framework.rapp.RApp`.
- Adding new interfaces or extending existing ones in the `oransim.interfaces` package.
- Creating new data collectors, analyzers, and visualizers in the `oransim.analytics` package.

Troubleshooting
---------------

If you encounter any issues while using ORANSim, please check the following:

- Make sure all dependencies are installed correctly.
- Verify that your configuration file is valid and conforms to the schema.
- Check the log files for any error messages.
- Consult the FAQ section below.
- If you still can't resolve the issue, please open an issue on the project's GitHub repository.

FAQ
---

**Q: How can I contribute to ORANSim?**

A: Please refer to the :ref:`contributing` guidelines for information on how to contribute to the project.

**Q: How do I cite ORANSim in my research paper?**

A: Please use the following citation:

.. code-block:: bibtex

    @misc{oransim,
      title = {{ORANSim: A 5G Open RAN Simulation Library}},
      author = {George Chidera Akor, Love Allen Chijioke Ahakonye, Dong-Seong Kim},
      year = {2025},
      howpublished = {\\url{https://github.com/Jupiter-Plantagenet/ORANSim}},
    }

**Q: Where can I find more examples?**

A: The `examples` directory in the ORANSim repository contains several example simulation scripts that demonstrate various features and use cases.

**Q: How can I get help if I have questions or encounter problems?**

A: Please open an issue on the project's GitHub repository, and we'll do our best to assist you.