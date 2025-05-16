import json
import os
from typing import Any, Dict, List, Optional, Union


###################################[ start BonfireFile ]##############################################
class BonfireFile:
    """
    Utility class for file operations in Bonfire.
    Handles saving and loading JSONL files.
    """

    @staticmethod
    def save(data: List[Dict[str, Any]], file_path: str) -> None:
        """
        Save data to a JSONL file.

        Args:
            data: List of dictionaries to save
            file_path: Path to the output file
        """
        # Ensure file has .jsonl extension
        if not file_path.endswith(".jsonl"):
            file_path = f"{file_path}.jsonl"

        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(os.path.abspath(file_path)), exist_ok=True)

        # Write data as JSONL
        with open(file_path, "w") as f:
            for item in data:
                f.write(json.dumps(item) + "\n")

    @staticmethod
    def load(file_path: str) -> List[Dict[str, Any]]:
        """
        Load data from a JSONL file.

        Args:
            file_path: Path to the input file

        Returns:
            List[Dict[str, Any]]: List of dictionaries loaded from the file

        Raises:
            ValueError: If the file is not a valid JSONL file
        """
        # Ensure file has .jsonl extension
        if not file_path.endswith(".jsonl"):
            raise ValueError(f"File {file_path} is not a JSONL file")

        # Check if file exists
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File {file_path} does not exist")

        # Read data from JSONL
        data = []
        with open(file_path, "r") as f:
            for line in f:
                line = line.strip()
                if line:  # Skip empty lines
                    try:
                        item = json.loads(line)
                        data.append(item)
                    except json.JSONDecodeError as e:
                        raise ValueError(f"Invalid JSON line in {file_path}: {e}")

        return data


###################################[ end BonfireFile ]##############################################
