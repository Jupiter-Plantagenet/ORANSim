import logging
import pandas as pd
from typing import Dict, Any, List, Union

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

class DataAnalyzer:
    """
    Provides methods for analyzing data collected during ORAN simulations.

    This class is designed to work with data collected by a `DataCollector` 
    (e.g., `CSVDataCollector`) and provides functions for common analysis tasks.
    """

    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)

    def load_data_from_csv(self, filepath: str) -> pd.DataFrame:
        """
        Loads data from a CSV file into a pandas DataFrame.

        Args:
            filepath (str): The path to the CSV file.

        Returns:
            pd.DataFrame: A pandas DataFrame containing the data.
        """
        try:
            df = pd.read_csv(filepath)
            self.logger.info(f"Data loaded from CSV file: {filepath}")
            return df
        except Exception as e:
            self.logger.error(f"Error loading data from CSV file {filepath}: {e}")
            return None

    def calculate_average(self, df: pd.DataFrame, column_name: str) -> float:
        """
        Calculates the average of a given column in a DataFrame.

        Args:
            df (pd.DataFrame): The DataFrame containing the data.
            column_name (str): The name of the column to calculate the average for.

        Returns:
            float: The average value of the column.
        """
        if column_name not in df.columns:
            self.logger.error(f"Column '{column_name}' not found in DataFrame.")
            return None
        try:
            average = df[column_name].mean()
            self.logger.info(f"Average of column '{column_name}': {average}")
            return average
        except Exception as e:
            self.logger.error(f"Error calculating average of column '{column_name}': {e}")
            return None
    
    def calculate_basic_statistics(self, df: pd.DataFrame, column_name: str) -> Dict[str, float]:
        """
        Calculates basic statistics (mean, median, standard deviation) for a given column.

        Args:
            df (pd.DataFrame): The DataFrame containing the data.
            column_name (str): The name of the column to calculate statistics for.

        Returns:
            Dict[str, float]: A dictionary containing the calculated statistics.
        """
        if column_name not in df.columns:
            self.logger.error(f"Column '{column_name}' not found in DataFrame.")
            return None

        try:
            stats = {
                "mean": df[column_name].mean(),
                "median": df[column_name].median(),
                "std": df[column_name].std(),
                "min": df[column_name].min(),
                "max": df[column_name].max(),
            }
            self.logger.info(f"Basic statistics for column '{column_name}': {stats}")
            return stats
        except Exception as e:
            self.logger.error(f"Error calculating statistics for column '{column_name}': {e}")
            return None
    
    def filter_by_time_range(self, df: pd.DataFrame, start_time: float, end_time: float, time_column: str = "timestamp") -> pd.DataFrame:
        """
        Filters the DataFrame to include only rows within a specific time range.

        Args:
            df (pd.DataFrame): The DataFrame to filter.
            start_time (float): The start time of the range.
            end_time (float): The end time of the range.
            time_column (str): The name of the column containing timestamps. Defaults to "timestamp".

        Returns:
            pd.DataFrame: A new DataFrame containing only the filtered rows.
        """
        if time_column not in df.columns:
            self.logger.error(f"Time column '{time_column}' not found in DataFrame.")
            return None
        
        try:
            filtered_df = df[(df[time_column] >= start_time) & (df[time_column] <= end_time)]
            self.logger.info(f"Data filtered by time range: {start_time} - {end_time}")
            return filtered_df
        except Exception as e:
            self.logger.error(f"Error filtering data by time range: {e}")
            return None

    def group_by_and_aggregate(self, df: pd.DataFrame, group_by_column: str, aggregations: Dict[str, Union[str, Callable]]) -> pd.DataFrame:
        """
        Groups the DataFrame by a given column and performs aggregations on other columns.

        Args:
            df (pd.DataFrame): The DataFrame to process.
            group_by_column (str): The name of the column to group by.
            aggregations (Dict[str, Union[str, Callable]]): A dictionary specifying the aggregations to perform.
                Keys are column names, and values are either aggregation function names (e.g., "mean", "sum")
                or callable aggregation functions.

        Returns:
            pd.DataFrame: A new DataFrame with the grouped and aggregated data.
        """
        if group_by_column not in df.columns:
            self.logger.error(f"Group-by column '{group_by_column}' not found in DataFrame.")
            return None

        try:
            grouped_df = df.groupby(group_by_column).agg(aggregations)
            self.logger.info(f"Data grouped by '{group_by_column}' and aggregated")
            return grouped_df
        except Exception as e:
            self.logger.error(f"Error grouping and aggregating data: {e}")
            return None
    
    # Add more analysis functions as needed for your specific use cases.