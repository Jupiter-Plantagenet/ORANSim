.. _contributing:

Contributing to ORANSim
========================

We welcome contributions to ORANSim! Whether you want to report a bug, suggest a 
new feature, or contribute code, please follow these guidelines:

1. **Report Bugs and Suggest Features:**

    Open an issue on the project's GitHub repository to report bugs or suggest 
    new features. Please provide a clear description of the issue or suggestion, 
    including steps to reproduce the bug or a detailed explanation of the 
    proposed feature.

2. **Set up a Development Environment:**

    *   Fork the ORANSim repository on GitHub.
    *   Clone your fork to your local machine:

        .. code-block:: bash

            git clone https://github.com/Jupiter-Plantagenet/ORANSim.git
            cd ORANSim

    *   Create a virtual environment:

        .. code-block:: bash

            python3 -m venv .venv

    *   Activate the virtual environment:

        *   On Linux/macOS:

            .. code-block:: bash

                source .venv/bin/activate

        *   On Windows:

            .. code-block:: bash

                .venv\\Scripts\\activate

    *   Install the required dependencies:

        .. code-block:: bash

            pip install -r requirements.txt

    *   Install ORANSim in editable mode:

        .. code-block:: bash

            pip install -e .

3. **Follow Coding Standards:**

    *   Adhere to the PEP 8 style guide.
    *   Use type hinting.
    *   Write comprehensive docstrings for all classes, methods, and functions.
    *   Use a linter like `flake8` to check your code.

4. **Write Tests:**

    *   Write unit tests and integration tests for any new code you add.
    *   Use the `pytest` framework for writing tests.
    *   Ensure that your tests cover all new functionality and edge cases.
    *   Run the tests locally before submitting a pull request:

        .. code-block:: bash

            pytest

5. **Submit a Pull Request:**

    *   Create a new branch for your changes:

        .. code-block:: bash

            git checkout -b feature/your-feature-name

    *   Commit your changes with clear and descriptive commit messages:

        .. code-block:: bash

            git commit -m "feat: Add support for new mobility model"

    *   Push your branch to your forked repository:

        .. code-block:: bash

            git push origin feature/your-feature-name

    *   Open a pull request on the main ORANSim repository.
    *   Provide a detailed description of your changes in the pull request.
    *   Address any feedback from the maintainers.

Thank you for contributing to ORANSim!