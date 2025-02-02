import logging
import csv
from typing import Dict, Any, Union, List
from abc import ABC, abstractmethod

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

class DataCollector(ABC):
    """
    Abstract base class for data collectors in the ORAN simulation environment.

    Data collectors are responsible for collecting and storing data generated during
    the simulation, such as KPIs, metrics, events, and other relevant information.
    """
    def __init__(self, output_path: str):
        self.output_path = output_path
        self.logger = logging.getLogger(self.__class__.__name__)

    @abstractmethod
    def collect_data(self, data: Dict[str, Any]):
        """
        Collects data generated during the simulation.

        Args:
            data (Dict[str, Any]): The data to collect. The structure of the data
                                    will depend on the specific type of data being
                                    collected (e.g., KPI, event, measurement).
        """
        pass

    @abstractmethod
    def write_data(self):
        """
        Writes the collected data to persistent storage (e.g., a file or database).

        This method might be called periodically or at the end of the simulation.
        """
        pass

class CSVDataCollector(DataCollector):
    """
    A data collector that stores data in CSV format.
    """

    def __init__(self, output_path: str):
        """
        Initializes the CSVDataCollector.

        Args:
            output_path (str): The path to the CSV file where data will be written.
        """
        super().__init__(output_path)
        self.data: List[Dict[str, Any]] = []

    def collect_data(self, data: Dict[str, Any]):
        """
        Collects data generated during the simulation.

        Args:
            data (Dict[str, Any]): The data to collect.
        """
        self.data.append(data)
        self.logger.debug(f"Collected data: {data}")

    def write_data(self):
        """
        Writes the collected data to a CSV file.
        """
        if not self.data:
            self.logger.warning("No data to write.")
            return

        try:
            with open(self.output_path, "w", newline="") as csvfile:
                # Assumes that all data dictionaries have the same keys
                fieldnames = self.data[0].keys()
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                writer.writeheader()
                for row in self.data:
                    writer.writerow(row)

            self.logger.info(f"Data written to CSV file: {self.output_path}")
        except Exception as e:
            self.logger.error(f"Error writing data to CSV file: {e}")

# Example usage (you can add this to your simulation setup):
# data_collector = CSVDataCollector("simulation_results.csv")

# Then, in your simulation, whenever you have data to collect:
# data_collector.collect_data({"timestamp": scheduler.env.now, "ue_id": ue.ue_id, "event": "handover"})

# Finally, at the end of your simulation (or periodically):
# data_collector.write_data()