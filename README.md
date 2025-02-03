
# ORANSim: A 5G Open RAN Simulation Library

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT) [![Documentation Status](https://readthedocs.org/projects/oransim/badge/?version=latest)](https://oransim.readthedocs.io/en/latest/?badge=latest) 

ORANSim is a comprehensive and extensible simulation library for 5G Open Radio Access Networks (ORAN). It is designed to be a powerful tool for researchers and engineers, enabling them to model, simulate, and analyze various aspects of ORAN systems with a focus on AI/ML-driven optimization and automation.

## Features

*   **Modular Architecture:** Easily extend and customize the simulation environment.
*   **Comprehensive ORAN Component Modeling:** Detailed models of Near-RT RIC, Non-RT RIC, O-CU-CP, O-CU-UP, O-DU, O-RU, and UEs.
*   **Standardized Interface Simulation:** Accurate representation of A1, E2, O1, F1, Xn, X2, and Open Fronthaul interfaces.
*   **Discrete-Event Simulation:** Scalable and efficient simulations using SimPy.
*   **AI/ML Integration:** Seamless integration with TensorFlow, PyTorch, and ONNX for developing and deploying intelligent xApps and rApps.
*   **Mobility Models:** Includes Random Walk, Random Waypoint, and Manhattan mobility models.
*   **Configurability:** Extensive configuration options via YAML files.
*   **Data Collection and Analysis:** Built-in tools for collecting, analyzing, and visualizing simulation data.
*   **O1 Interface Emulation:** Supports configuration management via NETCONF/YANG emulation.
*   **xApp/rApp Framework:** Provides a well-defined framework for creating and deploying xApps and rApps.
*   
-----------
## Installation

### Using pip (Recommended)

```
bash

pip install oransim
```

### From Source

1. Clone the ORANSim repository:

    ```bash
    git clone https://github.com/Jupiter-Plantagenet/ORANSim.git
    ```

2. Navigate to the project directory:

    ```bash
    cd ORANSim
    ```

3. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Install ORANSim in editable mode:

    ```bash
    pip install -e .
    ```

## Basic Usage

1. **Create a Configuration File:**

    Create a YAML file (e.g., `config.yaml`) that defines the simulation parameters, network topology, and other settings. Refer to the `config_schema.yaml` file and the documentation for details on the available configuration options.

    Example `config.yaml`:

    ```yaml
    simulation:
      duration: 100

    o_ru:
      o_ru_1:
        frequency: 3.5e9
        bandwidth: 100e6
        tx_power: 30
        cells:
          - cell_id: cell_1
            max_ues: 50
          - cell_id: cell_2
            max_ues: 75

    o_du:
      o_du_1:
        max_ues: 100
        cells:
          - cell_id: cell_3
            max_ues: 60
    ```

2. **Write a Simulation Script:**

    Create a Python script (e.g., `run_simulation.py`) that imports the necessary modules, loads the configuration, creates the simulation environment, and runs the simulation.

    Example `run_simulation.py`:

    ```python
    from oransim.simulation.scheduler import ORANScheduler
    from oransim.utils.config_loader import load_config
    # ... (Import other necessary classes) ...

    def main():
        # Load configuration
        config = load_config("config.yaml", "config_schema.yaml")

        # Create scheduler
        scheduler = ORANScheduler()

        # Create interfaces
        o1_interface = O1Interface("configs", "config_schema.yaml")  # Assuming configs directory for O1
        a1_interface = A1Interface(None, None)
        e2_interface = E2Interface(None, scheduler)

        # Create RICs
        near_rt_ric = NearRTRIC("near_rt_ric_1", a1_interface, e2_interface, scheduler)
        a1_interface.near_rt_ric = near_rt_ric  # Connect A1 interface to Near-RT RIC
        non_rt_ric = NonRTRIC(a1_interface, scheduler)
        a1_interface.non_rt_ric = non_rt_ric  # Connect A1 interface to Non-RT RIC
        non_rt_ric.add_managed_near_rt_ric(near_rt_ric)

        # Create nodes
        o_ru = O_RU(config["o_ru"]["o_ru_1"], scheduler)
        o_du = O_DU(config["o_du"]["o_du_1"], scheduler)

        # Apply O1 configuration
        o1_interface.apply_configs({"o_ru_1": o_ru, "o_du_1": o_du})
        # ... (Create and configure other components, add UEs, etc.) ...

        # Run simulation
        scheduler.run(until=config["simulation"]["duration"])

    if __name__ == "__main__":
        main()
    ```

3. **Run the Simulation:**

    ```bash
    python run_simulation.py
    ```

## Documentation

Detailed documentation, including a user manual, API reference, and tutorials, is available at [Remember to insert link to documentation Georgie! You would typically host your documentation on Read the Docs or a similar platform]. 

## Contributing

Contributions to ORANSim are welcome! Please refer to the [Contributing Guidelines](docs/contributing.rst) for information on how to contribute.

## License

ORANSim is licensed under the [MIT License](LICENSE) (Evaluate appropriate license later).

## Citation

If you use ORANSim in your research, please cite our paper:

```bibtex
@misc{oransim,
  title = {{ORANSim: A 5G Open RAN Simulation Library}},
  author = {George Chidera Akor, Love Allen Chijioke Ahakonye, Dong-Seong Kim},
  year = {2025},
  howpublished = {\\url{https://github.com/Jupiter-Plantagenet/ORANSim}},
}
```

